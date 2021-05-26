## 1.德州仪器视频解码器介绍

### 1.1支持的功能

- 高达1080p的H.264解码
- NV12（双平面）格式，8位内容支持
- 基于帧的解码
- 仅I帧解码
- I&P帧解码（有一个参考帧）
- 双通道解码，分辨率高达1080（1920x1080），每秒30帧
- 支持完全符合H.264规范的流；没有错误恢复支持。 

### 1.2不支持的功能
- 具有多个参考帧的I&P帧视频流
- B帧解码
- 非NV12像素格式
- 10位视频内容
- 由于不符合流而导致的崩溃的错误恢复
- 大于两个信道解码

### 1.3先决条件
#### 1.3.1确保视频流完全符合H.264规范
- 使用ffmpeg或JM解码器解码验证流，并尝试使用ffmpeg提供的ffplay实用程序播放位流
- 要生成自定义视频流，请使用任何版本的JM编码器生成*.h264/*.264文件。

#### 1.3.1如果视频流不符合H.264规范，需转码
- 对于任何容器流执行如下指令
```
ffmpeg -find_stream_info -i input.mkv -o output.h264
```
- 指令执行后日志将显示，当前流是否为H.264
```
Stream #0:0(und): Video.********
```
- 若有H.264，则从文件中复制视频流即可
```
    ffmpeg -i input.mkv -vcodec copy -acodec copy output.mp4 ffmpeg -i input.mp4 -c:v copy -bsf:v h264_mp4toannexb -an output.h264
```
- 如果它不包含H.264视频，那就不能将视频流从文件中复制出来。如果ffmpeg被编译为支持libx264，那么您可以从MP4V转码到H.264
```
ffmpeg -i file_example_MP4_480_1_5MG.mkv -an -vcodec libx264 -crf 23 output.h264
```
- 一旦生成H.264，则按上一步确认，是否符合H.264规范

### 1.4目录结构
| Video Codec Modules | Description |
| ---- | ---- |
|concerto 	|Makefile build infrastructure|
|docs 	|User documentation.|
|examples |	Application/Demo and Additional utility functions.|
|examples/apps/bios_cfg 	|Application bios configuration for TI-RTOS on R5F and A72.|
|examples/apps/common 	|Application common source code for TI-RTOS on R5F, and A72.|
|examples/apps/decoder 	|Application/Demo sample application for single and multichannel usecase.|
|examples/apps/mcu2_0 |	R5F configuration.|
|examples/apps/mpu1 |	A72 configuration.|
|examples/utils |	Additional utility functions used.|
|lib |	MM Driver fw library.|
|makerules |	Build utility.|
|out |	Build/Generated files and executables.|
|ti-img-encode-decode 	|MM Decoder Driver source code and firmware binary.|
|tools |	Scripts used to load and run the executables on CCS. |

### 1.5已知限制

- QCIF解析解码不工作
- OpenVx解码器节点中存在解码输出缓冲区上的memcpy
- 当前视频编解码器的内存分割设置仅支持两个同时通道

## 2.生成和运行指令
### 2.1生成指令
#### 2.1.1构建 TI MM H.264解码器步骤
##### 2.1.1.1Build Video Codec
```
cd video_codec

#For help on make options
make help

#To build the various components like pdk, video codecs for the first time
make codec_all 

#To build video codec library and executables incrementally for RTOS
make codec_apps
```

##### 2.1.1.2Build TIOVX
如果对TIOVX解码器一致性测试进行了编辑，请确保重建了TIOVX。
```
cd vision_apps

#To build TIOVX conformance tests 
make tiovx 
```
##### 2.1.1.3Build Vision Apps

```
cd vision_apps

#To build video codec into Processor SDK RTOS 
make vision_apps
```
#### 2.1.2清除TI MM H.264解码器步骤
```
cd video_codec

#To clean the various components like pdk, video codecs, etc
make codec_all_clean

#To do a clean build of video codecs
make codec_apps_clean
```
### 2.2运行步骤
要运行测试，首先要确保根据顶级SDK指令成功地创建和格式化了SD卡。
#### 2.2.1 安装到SD卡的步骤
```
cd vision_apps

#To install updated tiovx conformance tests and video_codec drivers 
make linux_fs_install_sd

#Make sure test streams are installed as well (one time for sd card setup)
make linux_fs_install_sd_test_data
```
#### 2.2.2 Run on EVM(嵌入式虚拟机？)
##### 2.2.2.1 Initialize Vision Apps
Boot the EVM with your SD card，then
```
cd /opt/vision_apps
source ./vision_apps_init.sh
```
##### 2.2.2.2 Run Single Stream
```
./vx_app_conformance.out --filter=tivxHwaVideoDecoder.SingleStreamProcessing
```
##### 2.2.2.3 Run Multi Stream
./vx_app_conformance.out --filter=tivxHwaVideoDecoder.MultiStreamProcessing

## 3.输出结果验证
- 将SD卡接到PC上，将输出文件从`/opt/vision_apps/test_data/output/`拷贝到自己的电脑上，并执行指令：
```
mplayer -demuxer rawvideo -rawvideo w=1280:h=720:format=nv12 decoder_output.yuv -fps 5
```
- 调整匹配解码码流的width/height，fps设置为适合观看的值

## 4.流配置
### 4.1解码一致性测试应用程序配置
vx_app_conformance运行的解码器测试位于：
```
psdk_rtos_auto_j7_xx/tiovx/kernels_j7/hwa/test/test_video_decoder.c
```
此测试读取一个配置文件，该文件可以更改以指定不同的测试配置参数以及输入流和分辨率。测试文件位于：
```
/opt/vision_apps/test_data/tivx/video_decoder/dec_single_channel.cfg
/opt/vision_apps/test_data/tivx/video_decoder/dec_multi_channel.cfg
```
配置了：测试配置、输入文件名和流的解析。
### 4.2测试应用程序配置
- num_iterations指定要解码的总帧数（不大于输入文件中的实际帧数；对于双通道，不大于输入文件中较短文件的实际帧数）。
### 4.3测试应用程序内部配置
- 如果需要解码大量帧，则可能需要修改test_video_decoder.c中的MAX_ITERATIONS，并且重构TIOVX。此变量指定分配用于跟踪用于读取输入文件的每帧比特流大小的数组的大小。
```
#define MAX_ITERATIONS     (100u)
```
- 默认情况下，测试应用程序还会将有限数量的输出帧转储到文件系统。你可以完全禁用这个功能
```
#define DUMP_DECODED_VIDEO_TO_FILE
```
- 或者可以通过更改以下内容来更改转储的帧数
```
#define NUM_FRAMES_DUMPED  (5u)
```
注意解码器的输出文件可能会变得非常大，尤其是在更高的分辨率下。

### 4.4更改测试流

要更改正在使用的测试流，请更新测试配置文件中的以下变量以匹配新的输入流：
- input_file
- width
- height
- bitstream_sizes
### 4.5Finding Bitstream Sizes
下面的一系列命令打印出输入文件中每个帧的大小。
```
ffprobe -show_packets <input_file>.264 | grep "size" | awk -F '=' '{print $2}'
```