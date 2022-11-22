# DuetCS - Automatic code style transfer
Coding style has direct impact on code comprehension. Automatically transferring code style to user's preference or consistency can facilitate project cooperation and maintenance, as well as maximize the value of open-source code. we used an unsupervised methods to transfer code to arbitrary code styles. We leverage Big Code resources to learn style and content embedding separately. We provides two modes - generation and retrieval to output a piece of code with the same functionality and the desired target style. 

![workflow](/doc/DuetCS.png "workflow")

## Datasets

### Big Code Resources

This dataset serves as unsupervised training data and the database for retrieval mode.

We use the Github repositories database - [Public Git Archive](https://github.com/src-d/datasets/tree/master/PublicGitArchive).

### Testing datasets
- Java dataset: Java-small (11 Java projects with about 700K code samples)
- JavaScript dataset: JSformat (19 top-starred JS repositories on GitHub)
- C++ dataset: Codeforces (20,721 C++ code samples)

## Dependencies
- Python 3.5.2
- MongoDB 4.2.12
- pymongo 3.9.0
- ANTLR4 (Java target)
- TensorFlow 1.10.0
- Numpy 1.13.3
- PyTorch 1.5.1

## Prepare database and training feature embedding module

`sh create_feature_em.sh path_to_your_database`

data_prepare.py: encode the original raw code to initial vector

feature.py: generate the initial feature embedding

siamese.py, training.py: train siamese network for the classification task


## Create feature embedding for input code/code examples in target style

`python3 testing.py path_to_code`

## Output results through two modes

generate transferred code through LSTM

`python 3 generation.py`

retrieve transferred code for the database and compare with geneartion mode to output the final result

`sh translate_retrieval.sh path_to_input target_language`

