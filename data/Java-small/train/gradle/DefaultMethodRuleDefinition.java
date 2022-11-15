/*
 * Copyright 2014 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.gradle.model.internal.inspect;

import com.google.common.collect.ImmutableList;
import net.jcip.annotations.ThreadSafe;
import org.gradle.api.Nullable;
import org.gradle.api.specs.Spec;
import org.gradle.internal.Cast;
import org.gradle.internal.Factory;
import org.gradle.model.Path;
import org.gradle.model.internal.core.ModelPath;
import org.gradle.model.internal.core.ModelReference;
import org.gradle.model.internal.core.rule.describe.MethodModelRuleDescriptor;
import org.gradle.model.internal.core.rule.describe.ModelRuleDescriptor;
import org.gradle.model.internal.method.WeaklyTypeReferencingMethod;
import org.gradle.model.internal.type.ModelType;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.Collections;
import java.util.List;

import static org.gradle.util.CollectionUtils.findFirst;

@ThreadSafe
public class DefaultMethodRuleDefinition<T, R, S> implements MethodRuleDefinition<R, S> {
    private ImmutableList<ModelReference<?>> references;
    private final Factory<? extends T> factory;
    private final WeaklyTypeReferencingMethod<T, R> method;

    private DefaultMethodRuleDefinition(Method method, ModelType<T> instanceType, ModelType<R> returnType, Factory<? extends T> factory) {
        this.factory = factory;
        this.method = WeaklyTypeReferencingMethod.of(instanceType, returnType, method);

        ImmutableList.Builder<ModelReference<?>> referencesBuilder = ImmutableList.builder();
        for (int i = 0; i < method.getGenericParameterTypes().length; i++) {
            Annotation[] paramAnnotations = method.getParameterAnnotations()[i];
            referencesBuilder.add(reference(paramAnnotations, i));
        }
        this.references = referencesBuilder.build();
    }

    public static <T> MethodRuleDefinition<?, ?> create(Class<T> source, Method method, Factory<? extends T> factory) {
        return innerCreate(source, method, factory);
    }

    private static <T, R, S> MethodRuleDefinition<R, S> innerCreate(Class<T> source, Method method, Factory<? extends T> factory) {
        ModelType<R> returnType = ModelType.returnType(method);
        return new DefaultMethodRuleDefinition<T, R, S>(method, ModelType.of(source), returnType, factory);
    }

    public Method getMethod() {
        return method.getMethod();
    }

    public String getMethodName() {
        return method.getName();
    }

    public ModelType<R> getReturnType() {
        return method.getReturnType();
    }

    @Nullable
    @Override
    public ModelReference<S> getSubjectReference() {
        return Cast.uncheckedCast(references.isEmpty() ? null : references.get(0));
    }

    @Override
    public List<ModelReference<?>> getTailReferences() {
        return references.size() > 1 ? references.subList(1, references.size()) : Collections.<ModelReference<?>>emptyList();
    }

    @Override
    public boolean isAnnotationPresent(Class<? extends Annotation> annotationType) {
        return getAnnotation(annotationType) != null;
    }

    @Override
    public <A extends Annotation> A getAnnotation(Class<A> annotationType) {
        for (Annotation annotation : method.getAnnotations()) {
            if (annotationType.isAssignableFrom(annotation.getClass())) {
                return Cast.uncheckedCast(annotation);
            }
        }
        return null;
    }

    public ModelRuleDescriptor getDescriptor() {
        return new MethodModelRuleDescriptor(method);
    }

    public ModelRuleInvoker<R> getRuleInvoker() {
        return new DefaultModelRuleInvoker<T, R>(method, factory);
    }

    public List<ModelReference<?>> getReferences() {
        return references;
    }

    private ModelReference<?> reference(Annotation[] annotations, int i) {
        Path pathAnnotation = (Path) findFirst(annotations, new Spec<Annotation>() {
            public boolean isSatisfiedBy(Annotation element) {
                return element.annotationType().equals(Path.class);
            }
        });
        ModelPath path = pathAnnotation == null ? null : ModelPath.path(pathAnnotation.value());
        ModelType<?> cast = ModelType.of(method.getGenericParameterTypes()[i]);
        return ModelReference.of(path, cast, String.format("parameter %s", i + 1));
    }
}
