# stm32f103c8t6的bsp移植（并非bsp制作）

## 一、库文件移植

### 1.1 rtthread内核移植

官方的rtthread源码的工程目录体积比较庞大，我们需要裁剪出我们需要的**rtt内核**，搭建一个**最小**的精简目录。

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-151041.png)

bsp文件夹里面已经包含了制作好的bsp文件以及一些模版文件（在进行bsp移植的时候，会借用到里面的一些文件）：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-145927.png)

接着将官方的rtthread源码进行裁剪，并输出一个精简目录，只留下：

#### 1.1.1 components

在RT-Thread看来，除了内核，其它第三方加进来的软件都是组件，比如gui、fatfs、lwip和finsh等。那么这些组件就放在components这个文件夹内，目前nano版本只放了finsh，其它的都被删除了，master版本则放了非常多的组件。finsh是RT- Thread组件里面最具特色的，它通过串口打印的方式来输出各种信息，方便我们调试程序。

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-193556.png)

#### 1.1.2 examples

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-200537.png)

#### 1.1.3 include

include目录下面存放的是RT-Thread内核的头文件，是内核不可分割的一部分。

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-193951.png)

#### 1.1.4 libcpu

RT-Thread是一个软件，单片机是一个硬件，RT- Thread要想运行在一个单片机上面，它们就必须关联在一起，那么怎么关联？还是得通过写代码来关联，这部分 关联的文件叫接口文件，通常由汇编和C联合编写。这些接口文件都是跟硬件密切相关的，不同的硬件接口文件是不一样的，但都大同小异。编写这些接口文件的过程我们就叫bsp的制作，bsp的制作过程通常由RT-Thread和mcu原厂的人来负责，制作好的这些接口文件就放在libcpu这个文件夹的目录下。通常网络上出现的叫“移植某某某RTOS到某某某MCU”的教程，其实准确来说，不能够叫“移植“，应该叫”使用官方的移植“（修改/添加/删除相应的接口文件），因为这些跟硬件相关的接口文件，RTOS官方都已经写好了，我们只是使用而已。

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-194658.png)

#### 1.1.5 src

src目录下面存放的是RT-Thread内核的源文件，是内核的核心。

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-194716.png)

#### 1.1.6 tools

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-200550.png)

#### 1.1.7 Kconfig

Kconfig文件先移植进来，后面第三章节再作解释。

如下是已经移植好的工程目录：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-153210.png)

#### 1.1.8 rtconfig.h

在rtthread文件夹同级目录下需要移植一个rtconfig.h文件

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250121-225301.png)

rtconfig.h文件中管理了一些宏定义（包含内核、线程通信、内存管理、组件等等），我们可以通过**增加/删除**一些宏来**打开/关闭**某些功能，还可以对一些宏定义替换的值进行修改：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250121-231139.png)



### 2.1 外设（HAL库）移植

新建一个board文件夹，该目录构造为：

| 项目                     | 需要修改的内容                           |
| ------------------------ | ---------------------------------------- |
| CubeMX_Config（文件夹）  | CubeMX工程                               |
| linker_scripts（文件夹） | bsp特定的链接脚本                        |
| board.c/h                | 系统时钟、GPIO初始化函数、芯片存储器大小 |
| Kconfig                  | 芯片型号、系列、外设资源                 |
| SConscript               | 芯片启动文件、目标芯片型号               |

#### 2.1.1 CubeMX工程

通过stm32cubemx来配置一个stm32f103c8t6的hal库工程：

1. 打开外部时钟、设置下载方式、打开串口外设（注意只需要选择串口外设引脚即可，无需配置其他参数）：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-215054.png)

2. 配置系统时钟

   ![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-232352.png)

3. 设置项目名称，并在指定地址重新生成 CubeMX 工程

   ![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-233110.png)

注意：在生成代码时，不要勾选以下选项（即：不让其生成单独的 .c/.h 驱动文件，直接全部更新到 rt-thread 要使用的 stm32xxx_hal_msp.c 文件中）

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-233519.png)

最终 CubeMX 生成的工程目录结构如下图所示：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-235555.png)

我们可以精简一下该目录的文件：

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250122-235638.png)

#### 2.2.2 链接脚本

##### 2.2.2.1 link.lds

##### 2.2.2.2 link.sct

##### 2.2.2.3 link.icf

#### 2.2.3 board文件



### 3.1 驱动移植





## 二、编译脚本移植

### 2.1 SCons脚本移植

#### 2.1.1 SConstruct

一般一个 bsp 中只有一个 SConstruct 文件

#### 2.1.2 SConscript

跟 SConstruct 文件所在目录有一个同级的 SConscript 文件，除此之外每一个需要编译的文件夹中都会有一个 SConscript 文件

### 2.2 rtconfig.py移植

![](F:\sdk-bsp-stm32f103c8t6-blue_pill\.pic\QQ20250121-225311.png)

rtconfig.py 这个脚本则是管理我们工程的工程通过何种编译器进行编译（目前脚本中可以设置 gcc、armcc、armclang、iccarm 这四种编译器，其中 armcc、armclang 是 MDK 的编译器，iccarm 是 EW 的编译器）

#### 2.2.1 gcc

#### 2.2.2 armcc

#### 2.2.3 iccarm



## 三、Kconfig脚本移植

