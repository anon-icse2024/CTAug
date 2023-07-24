# CTAug - Data augmentation for code translation
Code translation is needed in many use cases, both in academia and industry. This application rewrites a piece of code in another user-preferred language for further usage. Manual code translation is resource-consuming. A supervised code translation model can automate this process. However, it faces the problem of a shortage of training data. We experiment with different existing data augmentation methods on supervised code translation, and propose our own augmentation data generating rules, and a retrieval-based approach, which is shown in the following figure:

![workflow](/doc/complete_workflow.png "workflow")

## Datasets

### Dataset to augment
- Java to C# dataset: a parallel dataset of translating Java to C#. It contains six open-source projects, which have both a Java and a C# implementation (16,996 methods in total)

### Big Code Resources for Retrieval-based Augmentation

We use the Github repositories database - [Public Git Archive](https://github.com/src-d/datasets/tree/master/PublicGitArchive).

## Dependencies
- Python 3.5.2
- MongoDB 4.2.12
- pymongo 3.9.0
- ANTLR4 (Java target)
- TensorFlow 1.10.0
- Numpy 1.13.3
- Keras 2.2.2

## Rule-based method
We created three rules to generate augmentation data based on the original data: reverse, merge, and split.

To implement the rule, directly run the rule/rules on the code file, for example:

`python3 reverse_rule.py path_to_your_original_training_code`

## Retrieval-based augmentation method

We directly implement RPT for mono-language code retrieval, and BigPT for cross-language code retrieval.
(https://github.com/LUH-DBS/Binger/tree/main/BigPT)

## Performance comparison of different augmentation methods

![performance](/doc/performance.png "performance")

