# Face-Recognition by Mustafa Karakaş

## GUI Ekran Görüntüleri


| Giriş Ekranı                               | Kayıt Ekranı                                  |
|--------------------------------------------|-----------------------------------------------|
| ![](src/resources/projectImages/login.png) | ![](src/resources/projectImages/register.png) |

| Şifre Yenile                                   | Şifre Sıfırla                                  |
|------------------------------------------------|------------------------------------------------|
| ![](src/resources/projectImages/renewPass.png) | ![](src/resources/projectImages/resetPass.png) |

| Ana Ekran                                       | Veri Ekle                                    |
|-------------------------------------------------|----------------------------------------------|
| ![](src/resources/projectImages/mainScreen.png) | ![](src/resources/projectImages/dataAdd.png) |

| Veri Sil                                        | Veri Bilgisi                                  |
|-------------------------------------------------|-----------------------------------------------|
| ![](src/resources/projectImages/dataDelete.png) | ![](src/resources/projectImages/dataInfo.png) |

| Model Eğitimi                                   | Model Sil                                        |
|-------------------------------------------------|--------------------------------------------------|
| ![](src/resources/projectImages/modelTrain.png) | ![](src/resources/projectImages/modelDelete.png) |

| Model Bilgisi                                  | 
|------------------------------------------------|
| ![](src/resources/projectImages/modelInfo.png) |

| Model Bilgi Grafiği                        | 
|--------------------------------------------|
| ![](src/resources/projectImages/graph.png) |

| Test Web                                     | Yerel Klasör Dosya Seçimi                        |
|----------------------------------------------|--------------------------------------------------|
| ![](src/resources/projectImages/testWeb.png) | ![](src/resources/projectImages/localFolder.png) |

| Test Url Image                                                                                            | Test Url Youtube                                                                                         |
|-----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| ![](src/resources/projectImages/testUrlImage0.png)<br/>![](src/resources/projectImages/testUrlImage1.png) | ![](src/resources/projectImages/testYoutube0.png) <br/>![](src/resources/projectImages/testYoutube1.png) |

### Model isimlendirmesi:

| Veriseti Türü | Veriseti Adı | Veriseti Versiyonu | Veri Çeşit Sayısı | Batch Boyutu | Epoch Sayısı | Girdi Boyutu (GxY) | 3 Karakterli Rastgele Dize | Model Uzantısı | Elde Edilen Model İsmi                 |
|---------------|--------------|--------------------|-------------------|--------------|--------------|--------------------|----------------------------|----------------|----------------------------------------|
| face          | faceset      | v1                 | 20                | 8            | 30           | 128x128            | nap                        | .h5            | face_faceset_v1_20_8_30_128x128_nap.h5 |
| face          | faceset      | v1                 | 20                | 32           | 3            | 128x128            | tga                        | .h5            | face_faceset_v1_20_32_3_128x128_tga.h5 |
| face          | faceset      | v1                 | 20                | 8            | 2            | 128x128            | wep                        | .h5            | face_faceset_v1_20_8_2_128x128_wep.h5  |

- 'admin' kullanıcı adı, şifre : admin123, admin123
- Roller : ADMIN, USER, None