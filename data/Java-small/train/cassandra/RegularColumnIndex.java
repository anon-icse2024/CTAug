/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.cassandra.index.internal.composites;

import java.nio.ByteBuffer;

import org.apache.cassandra.db.*;
import org.apache.cassandra.db.rows.Cell;
import org.apache.cassandra.db.rows.CellPath;
import org.apache.cassandra.db.rows.Row;
import org.apache.cassandra.index.internal.CassandraIndex;
import org.apache.cassandra.index.internal.IndexEntry;
import org.apache.cassandra.schema.IndexMetadata;

/**
 * Index on a REGULAR column definition on a composite type.
 *
 * A cell indexed by this index will have the general form:
 *   ck_0 ... ck_n c_name : v
 * where ck_i are the cluster keys, c_name the last component of the cell
 * composite name (or second to last if collections are in use, but this
 * has no impact) and v the cell value.
 *
 * Such a cell is indexed if c_name == columnDef.name, and it will generate
 * (makeIndexColumnName()) an index entry whose:
 *   - row key will be the value v (getIndexedValue()).
 *   - cell name will
 *       rk ck_0 ... ck_n
 *     where rk is the row key of the initial cell. I.e. the index entry store
 *     all the information require to locate back the indexed cell.
 */
public class RegularColumnIndex extends CassandraIndex
{
    public RegularColumnIndex(ColumnFamilyStore baseCfs, IndexMetadata indexDef)
    {
        super(baseCfs, indexDef);
    }

    public ByteBuffer getIndexedValue(ByteBuffer partitionKey,
                                      Clustering clustering,
                                      CellPath path,
                                      ByteBuffer cellValue)
    {
        return cellValue;
    }

    public CBuilder buildIndexClusteringPrefix(ByteBuffer partitionKey,
                                               ClusteringPrefix prefix,
                                               CellPath path)
    {
        CBuilder builder = CBuilder.create(getIndexComparator());
        builder.add(partitionKey);
        for (int i = 0; i < prefix.size(); i++)
            builder.add(prefix.get(i));

        return builder;
    }

    public IndexEntry decodeEntry(DecoratedKey indexedValue, Row indexEntry)
    {
        Clustering clustering = indexEntry.clustering();
        ClusteringComparator baseComparator = baseCfs.getComparator();
        CBuilder builder = CBuilder.create(baseComparator);
        for (int i = 0; i < baseComparator.size(); i++)
            builder.add(clustering.get(i + 1));

        return new IndexEntry(indexedValue,
                                clustering,
                                indexEntry.primaryKeyLivenessInfo().timestamp(),
                                clustering.get(0),
                                builder.build());
    }

    public boolean isStale(Row data, ByteBuffer indexValue, int nowInSec)
    {
        Cell cell = data.getCell(indexedColumn);
        return cell == null
            || !cell.isLive(nowInSec)
            || indexedColumn.type.compare(indexValue, cell.value()) != 0;
    }
}
