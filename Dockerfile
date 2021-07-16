FROM debian:testing
MAINTAINER Mahefa Randimbisoa <dotmg@users.sourceforge.net>

RUN mkdir -p /opencv/build
COPY 4.5.3.tar.gz *.py /opencv
RUN apt-get update -q -y && apt-get install -y \
	build-essential \
	cmake \
	git \
	libgtk2.0-dev \
	pkg-config \
	libavcodec-dev \
	libavformat-dev \
	libswscale-dev \
	python-dev \
#	python-numpy \
	libtbb2 \
	libtbb-dev \
	libjpeg-dev \
	libpng-dev \
	libtiff-dev \
	liblapack-dev \
	python3-pip \
	ffmpeg \
	libavcodec-dev \
	libavfilter-dev \
	libv4l-dev \
	libx264-dev \
	x264 \
	libx264-160 \
#	libjasper-dev \
	libdc1394-22-dev;
RUN cd /opencv && tar xf /4.5.3.tar.gz && mv opencv-* opencv && pip install numpy;
RUN mkdir /opencv/opencv/build && \
	cd /opencv/opencv/build && \
	cmake \
		-D CMAKE_BUILD_TYPE=RELEASE  \
		-D BUILD_PYTHON_SUPPORT=ON \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D BUILD_opencv_python3=ON \
		-D PYTHON_3_EXECUTABLE=/usr/bin/python3 \
		-D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
		-D WITH_FFMPEG=ON \
		-D WITH_OPENCL=ON \
		-D WITH_OPENGL=ON \
		-D WITH_V4L=ON \
		-D WITH_LAPACK=ON \
		-D WITH_GSTREAMER=ON \
		.. \
	;
RUN cd /opencv/opencv/build && \
	make && \
	make install;
