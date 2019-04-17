# ICLR2019-Reproducibility-Challenge

Paper: [ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness](https://openreview.net/forum?id=Bygh9j09KX)
Code: [texture-vs-shape](https://github.com/rgeirhos/texture-vs-shape)
1. 确定重复的主要论点，找出文中依据与实验数据
1. 总结文章的逻辑思路


---
## abstract
论文定量地研究了 CNNs 在识别物体时，图像的纹理和形状如何影响决策。
作者发现，基于ImageNet训练的CNN非常喜欢依据纹理做决策，而不是形状，这与人类的行为相反。
同时，作者阐释了相同的模型（ResNet-50）可以学习基于纹理的特征表示（使用ImageNet数据），也可以学习基于形状的特征表示（使用stylized ImageNet数据）。
这样得到的模型更接近人类的行为，并且有意想不到的好处。例如，提高在物体识别中的表现，对多种图像扭曲有前所未见的鲁棒性，突出了形状表示具有优越性。

## introduction
CNN可以有效识别物体。一个直觉上的解释是CNN不断组合低级的特征（如边缘）得到复杂形状（如车轮、车窗），直到物体（如汽车）可以恰好与其他类区别开。
【例子1，2】
这种解释称之为形状假说。

这个假设有大量的经验证据支持。【例子1，2，3，4】

另外，其他的研究表明物体的纹理对CNN识别物体也很重要。【例子1，2，3，4，5】
总之，似乎局部的纹理真的提供了足够的物体类别信息。
这意味着，ImageNet的分类 原则上可以只使用纹理识别来完成。
作者相信，使用CNN识别物体时，物体的纹理比全局的形状更重要。
这是纹理假说。

解决这两个互相矛盾的假说对理解CNN意义很大。
这项工作中，作者设计了直观的实验来解决这个问题。
使用风格迁移可以得到形状和纹理相矛盾的图案，用来定量分析人和CNN在物体识别中的bias。
实验结果表明，纹理假说更有可能正确。
此外，作者另外两个贡献是changing biases（例如，把CNN原本基于纹理决策改为基于形状决策）和探索changing biases的好处。
作者发现如果使用合适的数据集，可以把CNN原本基于纹理决策改为基于形状决策。主要基于形状决策的CNN更加鲁棒。

## methods
### 心理学实验
pass
### 数据集
为了评估texture biases 和 shape biases，作者做了6个主实验和3个控制实验。
前五个实验是简单的物体识别（如图2所示），改变原图，再尝试识别。
注意，实验使用的原图是所有4个CNN都能正确识别的。
这是为了与第6个实验对照，方便解释结果。
第6个实验使用纹理与形状矛盾的图片，要求CNN尝试分类。
只有原图是所有4个CNN都能正确识别的，才能保证该实验的重心在验证纹理假说或形状假说。
该试验要求人类被试保持绝对中立态度（即不要偏向形状或纹理）。
因为没有正确的答案，作者关注被试的主观想法。

### stylized-ImageNet （SIN）
基于ImageNet得到的新数据集。去除图像的纹理，并用随机的风格替代（使用AdaIN，如图3所示）。
## results
### 人类和IMAGENET训练的CNNS中的纹理和形状偏见（TEXTURE VS SHAPE BIAS）
几乎所有图像都被正确识别。
灰度图仍然同时含有形状和纹理信息，因此识别结果与使用原图一样好。
在silhouette的图中，物体的边缘用黑色填充，CNN准确率比人类低很多。
silhouette使得边缘刺激更为明显，这说明人类对少量纹理或没有纹理的图像表现更好。
这些实验中的一个困惑是CNN往往不能很好地应对领域迁移（即对训练图片做较大的风格改动会显著降低表现）。

因此，作者设计了一个cue conflict实验（即识别纹理与形状矛盾的图片），这样可以看出CNN主要依赖的特征。
图4显示了实验结果。人类有一个显著的shape bias（95.9% 的准确率）。
而CNN恰好相反，它有一个显著的texture bias。【具体数据】

### 克服CNN的 texture bias
心理学实验表明CNN有显著的texture bias。
其中一个原因可能是训练任务本身。可以只使用局部信息就在ImageNet上取得高准确率。
换句话说，局部特征的组合就已经足够，而不需要整合和区分全局形状。
为了验证这个假说，作者在stylized-ImageNet （SIN）数据集上训练了一个ResNet-50。

ResNet-50训练效果见表1。作为对比，ResNet-50在ImageNet（IN）上有92.9%的Top-5准确率。
这说明SIN是比IN更难的任务，因为图像纹理不再有参考价值。
有趣的是，IN上得到的特征（feature）很难适用于SIN（只有16.4%的Top-5准确率）。
反过来，SIN的特征在IN上有82.6%的准确率（未精细调参）。

为了确定局部纹理特征是否足够用于解决SIN，作者评估了BagNet在其上的表现。【BagNet简介】
9x9像素感受视野的BagNet在ImageNet（IN）上有70.0%的Top-5准确率，但在SIN上表现非常差，只有10.0%的Top-5准确率。
这说明SIN的确去除了局部的纹理信息，以强迫网络整合大范围的空间信息（long-range spatial information）。

更重要的是，在第6个实验中，基于SIN训练的ResNet-50有更强的形状偏见（shape bias）（如图5）。

### 形状表示（shape-based representation）的准确率和鲁棒性
增加形状偏见（shape bias），得到的shifted representation是否会影响CNN的鲁棒性或准确率？
除了SIN和IN，作者额外分析了两个联合训练方案:
1. 在SIN和IN上联合训练
1. 在SIN和IN上联合训练，并用IN调参（下称Shape-ResNet）

作者做了三个实验，将得到的模型与普通的ResNet-50比较（表2）。
- IN上的表现。
Shape-ResNet的表现比普通的ResNet好，说明SIN可能是有用的数据增强。
- 迁移学习（Pascal VOC 2007和MS COCO）。

- 对扰乱的鲁棒性。
作者测试了模型对多种图像扭曲的鲁棒性（图6）。在SIN上训练的网络基本上总是比IN上的好（低通滤波处理的图像是例外）。
## discussion

## conclusion
作者证实今天的机器识别基本上依赖物体的纹理而不是大部分人认同的形状。
作者展示了使用基于形状表示决策的鲁棒性和好处。
作者预见他们的发现和他们开放的模型和代码将达成3个目标：
1. 对CNN的特征表示和偏差（bias）有更深入的理解。
1. 向获得更合理的人类视觉物体识别模型迈出了一步。 
1. 这是未来工作的起点，其中的领域知识（domain knowledge）表明基于形状的表示可能比基于纹理的表示更有用。
