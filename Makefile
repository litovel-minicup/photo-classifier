all: download

download: a0ae577d85.jpg a0b8ffa2c7.jpg a0cc8c42de.jpg a0dfbb3778.jpg a0f91acf87.jpg a00e09610b.jpg a0173b969f.jpg a02a4a9331.jpg a051ba7c12.jpg a053b3c5ab.jpg a056236458.jpg a06818eda7.jpg a1af2a5a95.jpg a1ef763f6b.jpg a13d332d94.jpg a17b998c94.jpg a17695ef5f.jpg a194a4de5c.jpg a2aa8aded5.jpg a2a0fa8436.jpg a2bd760d9d.jpg a2d46bdbae.jpg a2f3ff1dce.jpg a202664f29.jpg a2152fd488.jpg a2194c106e.jpg a2314dce80.jpg a26b18a7de.jpg a26e93162c.jpg a268d7652e.jpg a28d840178.jpg a28277e565.jpg a289457de5.jpg a295143529.jpg a30a144ef5.jpg a32db2c7a4.jpg a33742349c.jpg a39ca83eb2.jpg a393de6636.jpg a4aa38bc30.jpg a412ff6239.jpg a4224aa01d.jpg a42514c06c.jpg a43363b60a.jpg a4648e24f3.jpg a4756ae8c7.jpg a4756b08c8.jpg a49dfef3b6.jpg b1da6958ad.jpg b1ea887d3c.jpg b1fad8abf3.jpg b13df6e5a5.jpg b138d92b81.jpg b1392c28e7.jpg b145fcf62b.jpg b18b757d4c.jpg b184673f0e.jpg  

install:
	test -d .venv || pyvenv .venv
	./.venv/bin/pip install -r requirements.txt
	make build

prepare:
	mkdir -p data/

%.jpg: prepare
	wget https://minicup.tatranlitovel.cz/media/medium/$@ -O data/$@ -o /dev/null

clean:
	rm -rf data/


build:
	(cd minicup_photo_classifier/lib/nms_cython && python setup.py build_ext --inplace)
	(cd minicup_photo_classifier/lib/multicut_cython && python setup.py build_ext --inplace)

.ONESHELL:
download-models:
	mkdir -p models && cd models
	curl -L -O https://datasets.d2.mpi-inf.mpg.de/deepercut-models-tensorflow/coco-resnet-101.data-00000-of-00001
	curl -L -O https://datasets.d2.mpi-inf.mpg.de/deepercut-models-tensorflow/coco-resnet-101.meta
	curl -L -O https://datasets.d2.mpi-inf.mpg.de/deepercut-models-tensorflow/coco-resnet-101.index
	curl -L -O https://datasets.d2.mpi-inf.mpg.de/deepercut-models-tensorflow/pairwise_coco.tar.gz
	tar xvzf pairwise_coco.tar.gz
