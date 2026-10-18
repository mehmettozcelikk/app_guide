# GitHub yükleme - güvenli adımlar

Bu dosya öneridir; komutlar kullanıcının bilgisayarındaki mevcut proje dizininden çalıştırılmalıdır.

1. `.env` içindeki anahtarı GitHub'a eklemeyin. `.gitignore` satırının `.env` içerdiğini doğrulayın.
2. `python -m unittest discover -s tests -v` çalıştırın.
3. `git init` (ilk kez ise), `git add .`, `git status --short`, `git ls-files` komutlarını kullanın.
4. **`git ls-files` çıktısında `.env` veya API anahtarı içeren herhangi bir dosya varsa COMMIT ETMEYİN.**
5. `git commit -m "SIC SDG GenAI hackathon prototype"`
6. GitHub'da boş bir repo oluşturup verilen HTTPS adresiyle: `git branch -M main`, `git remote add origin https://github.com/USERNAME/REPO.git`, `git push -u origin main`.
7. GitHub sayfasını gizli sekmede açarak README, `docs/report.pdf`, promptlar, örnekler ve test sonuçlarının görüntülendiğini doğrulayın.
8. `.env` yanlışlıkla bir kez bile commit edildiyse anahtarı Google AI Studio üzerinden iptal edip yenisini oluşturun.
9. İngilizce sunum ve ~5 dakikalık İngilizce video hazırlayıp bağlantıların herkese görünür olduğundan emin olun; teslim formuna zamanında girin.

Kodu/yüklemeyi yapmak ücretsiz API katmanına ücretli erişim tanımlamaz, ancak GitHub'ın görünürlüğünü ve sağlayıcının ücretsiz kota durumunu kendiniz kontrol edin.
