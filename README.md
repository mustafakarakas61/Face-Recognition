# Face-Recognition by Mustafa Karakaş

## GUI Ekran Görüntüleri

| Ana Ekran                               | Yüz Ekle                              |
|-----------------------------------------|---------------------------------------|
| ![](utils/projectImages/mainScreen.png) | ![](utils/projectImages/addFace.png)  |

| Model Eğitimi | Model Sil       |
|---------------|-----------------|
| ![](utils/projectImages/modelTrain.png)  | ![](utils/projectImages/modelDelete.png)  |

| Test Web                              | Yerel Klasör Dosya Seçimi                |
|---------------------------------------|------------------------------------------|
| ![](utils/projectImages/testWeb.png)  | ![](utils/projectImages/localFolder.png) |

| Test Url Image                                                                            | Test Url Youtube                                                                         |
|-------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| ![](utils/projectImages/testUrlImage0.png)<br/>![](utils/projectImages/testUrlImage1.png) | ![](utils/projectImages/testYoutube0.png) <br/>![](utils/projectImages/testYoutube1.png) |

### Model isimlendirmesi:

| Veriseti Türü | Veriseti Adı | Veriseti Versiyonu | Veri Çeşit Sayısı | Batch Boyutu | Epoch Sayısı | Girdi Boyutu (GxY) | 3 Karakterli Rastgele Dize | Model Uzantısı | Elde Edilen Model İsmi                  |
|---------------|--------------|--------------------|-------------------|--------------|--------------|--------------------|----------------------------|----------------|-----------------------------------------|
| face          | faceset      | v1                 | 20                | 32           | 50           | 128x128            | dvy                        | .h5            | face_faceset_v1_20_32_50_128x128_dvy.h5 |
| face          | faceset      | v1                 | 20                | 8            | 30           | 128x128            | esy                        | .h5            | face_faceset_v1_20_8_30_128x128_esy.h5  |