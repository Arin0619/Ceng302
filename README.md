# Ceng302 — Student Sandbox

Bu depo eğitim amaçlı, küçük Python örnekleri ve alıştırmalar içerir.
Aşağıda her dosyanın amacı, nasıl çalıştırılacağı, testler ve güvenlik notları bulunmaktadır.

## Proje Özeti
- Basit fonksiyonel örnekler, hataları bulup düzeltme (debug), test ekleme ve güvenlik iyileştirmeleri için hazırlanmış bir çalışma dizini.
- Ana hedefler: kodu daha modüler ve test edilebilir hale getirmek; yaygın güvenlik hatalarını tespit etmek ve düzeltmek.

## Dosya listesi ve açıklamaları
- `spaghetti_logic.py`
  - Refaktör edilmiş modül; veri işleme boru hattına ayrılmıştır.
  - Sağlanan fonksiyonlar: `apply_markup(value, rate=0.15)`, `format_total(value, prefix='Total:')`, `log_results(results, filename='log.txt')`, `process_data(data, rate=0.15, log_file='log.txt', verbose=True)`.
  - Amaç: okuması zor "spaghetti" kodu küçük, tek sorumluluklu fonksiyonlara bölmek.

- `failing_calculator.py`
  - Orijinal olarak [10, 5, 0] girdisinde çöküyordu (sıfıra bölme).
  - Yeni `average_ratios(numbers)` fonksiyonu şöyle davranır:
    - Sıfırları atlar (0 için 100/x hesaplanmaz).
    - Eğer hiç non-zero eleman yoksa `ValueError` fırlatır.
    - Girdi tipi kontrolü yapar ve geçersiz öğe varsa `TypeError` fırlatır.

- `test_failing_calculator.py`
  - `failing_calculator.py` için birim testleri içerir (normal, tüm sıfırlar, geçersiz girdiler).

- `mystery_module.py`
  - `fn_x(a, b, c)` fonksiyonu; bir kuadratik denklem köklerini hesaplar (quadratic formula).
  - Hesaplama: diskriminant `d = b**2 - 4*a*c`. Eğer `d < 0` ise `None` döner (karmaşık kökleri dışlar).
  - Aksi halde `(root1, root2)` tuple'ı döner:
    - `(-b + sqrt(d)) / (2*a)` ve `(-b - sqrt(d)) / (2*a)`
  - Not: `a == 0` durumunda şu an bir kontrol yok; bu durumda `ZeroDivisionError` oluşabilir — dikkat edilmeli.

- `secret_leak.py`
  - Eski versiyonda dosyada sabit (hard-coded) bir AWS anahtarı vardı.
  - Dosya güvenli kullanım için yeniden düzenlendi: `AWS_SECRET_KEY` artık `os.environ.get('AWS_SECRET_KEY')` ile alınıyor ve değer kesinlikle stdout'a yazdırılmıyor.
  - Ayrıca `SECURITY_ISSUE_secret_leak.md` dosyası eklendi (risk, çözüm adımları, öneriler).

- `test_spaghetti_logic.py`
  - `spaghetti_logic.py` içindeki temel fonksiyonları test etmeye yönelik unittest testleri içerir.

- `SECURITY_ISSUE_secret_leak.md`
  - Repository'de tespit edilen secret-exposure ile ilgili yerel bir güvenlik issue dökümanıdır. İçinde hızlı çözüm adımları, tavsiyeler ve önceliklendirme yer alır.

## Nasıl çalıştırılır (geliştirici yönergeleri)
Ön koşul: Python 3.8+ (venv önerilir).

1. Depoya gidin:
```powershell
cd 'C:\Users\arind\Desktop\mcp-student-sandbox'
```

2. (Opsiyonel) Sanal ortam oluşturup etkinleştirin:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

3. Örnek modülleri çalıştırma:
- `failing_calculator.py` (örnek):
```powershell
python failing_calculator.py
```
- `spaghetti_logic.py` (örnek):
```powershell
python spaghetti_logic.py
```

4. `secret_leak.py` çalıştırmadan önce ortam değişkeni ayarlayın (PowerShell örneği):
```powershell
$env:AWS_SECRET_KEY = 'your_aws_secret_here'
python -c "import secret_leak; secret_leak.connect()"
```
Not: Gerçek anahtarları bu repoya kesinlikle commit etmeyin. Eğer bir anahtar kazara commit edildiyse, o anahtarı hemen rotate edin.

## Testler
Birim testleri Python'un `unittest` ile yazıldı. Tüm testleri çalıştırmak için:

```powershell
python -m unittest -v
```

Not: Bu ortamda testleri çalıştırmayı denedim ama Python yüklü değildi; yerel makinenizde yukarıdaki adımla çalıştırabilirsiniz.

## Kod analizi — kısa özet ve öneriler
- `mystery_module.fn_x(a,b,c)`:
  - Ne yapar: kuadratik denklemin gerçek köklerini döndürür veya negatif diskriminantta `None` döner.
  - Öneriler:
    - `a == 0` durumunu kontrol et (çünkü `2*a`'ya bölme yapılırken hata oluşur).
    - Karmaşık kökleri isterseniz `cmath` kullanarak döndürebilirsiniz; yoksa mevcut davranışı yeterli.

- `failing_calculator.average_ratios`:
  - Düzeltildi: sıfırları atlar ve uygun hata türleri fırlatır.
  - Edge case: tüm elemanlar sıfır ise `ValueError` fırlatılır; bu davranış test edildi.

- `spaghetti_logic`:
  - Başlıca amaç refaktör; işlem adımlarını ayırarak test edilebilirlik ve bakım kolaylığı sağlandı.
  - `log_results` dosya yolunun yazılabilirliği ve JSON-lines formatına geçme opsiyonu değerlendirilebilir (README'da öneri).

## Kısa "contract" (seçili fonksiyonlar)
- average_ratios(numbers)
  - Input: iterable of numbers
  - Output: float (ortalama) or raises on invalid conditions
  - Error modes: TypeError for invalid types; ValueError if no non-zero items

- process_data(data, rate, log_file, verbose)
  - Input: iterable of numbers
  - Output: list of floats (markup applied)
  - Side effects: appends list repr to `log_file`
  - Errors: TypeError on invalid items

## Güvenlik notları ve öneriler
- Hiçbir zaman gerçek gizli anahtarları (API key, secret, password) kaynak koduna commit etmeyin.
- Mevcut `secret_leak.py` sabit anahtar kaldırıldı. Eğer gerçek bir anahtar kazara commit edildiyse:
  1. Anahtarı derhal rotate edin.
  2. Repo geçmişinde anahtarın izlerini temizleme (bfg/git-filter-repo) ve anahtarın kullanımını denetleme (audit) yapın.
- Önerilen araçlar: `detect-secrets`, `pre-commit` ile `detect-secrets` hook'u, GitHub secret scanning.

## Katkıda bulunma
- Küçük değişiklikler için fork → branch → PR akışı uygundur.
- Test ekleyin ve `python -m unittest -v` ile testlerin geçtiğinden emin olun.

## Branchler ve yapılan lokal değişiklikler
- `fix/average_ratios-zero-division`: `failing_calculator.py` hatası için düzeltme ve test eklendi.
- `security/remove-hardcoded-secret`: `secret_leak.py`'de sabit anahtar kaldırıldı ve `SECURITY_ISSUE_secret_leak.md` eklendi.

## Sonraki önerilen adımlar
- (Yüksek öncelik) GitHub üzerinde secret scanning aktif edin ve mevcut anahtarları/commit geçmişini kontrol edip gerekiyorsa rotate edin.
- (Orta) `log_results` çıktısını JSON-lines formatına çevirin (parsing kolaylığı için).
- (İsteğe bağlı) GitHub Actions CI ekleyin: push/PR sırasında `python -m unittest -v` çalışsın ve basit secret-scan job'u ekleyin.

---

Hazır olduğunuzda; isterseniz ben:
- CI (GitHub Actions) ekleyebilirim,
- PR/Issue açma komutlarını sizin adınıza çalıştırıp sonucu paylaşabilirim (push yetkisine ihtiyacım olacak),
- veya README üzerinde farklı dillerde (İngilizce) versiyon ekleyebilirim.
