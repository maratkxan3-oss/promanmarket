"""Bir martalik xavfsiz "seed": ProMan Electronics do'koniga Uzum Market'dan
saralangan 2-PARTIYA — yana 60 xil kunlik zarur elektronika va maishiy
texnika mahsulotini qo'shadi.

Bot ishga tushganda chaqiriladi. Mantiq [seed_bikes.seed_products] da —
mavjud mahsulotlarga TEGMAYDI, faqat hali yo'q bo'lganlarini qo'shadi,
shuning uchun bot necha marta qayta ishga tushsa ham takror qo'shilmaydi.

Nom, narx va rasmlar Uzum Market'dan (images.uzum.uz CDN) to'g'ridan-to'g'ri
har bir mahsulot sahifasidan olingan — nom, narx va rasmlar bir-biriga mos.
Ko'p mahsulotda 3 ta rasm, ba'zilarida do'kon bergancha 1-2 ta.
"""

import logging

from app.seed_bikes import seed_products
from app.seed_proman import _find_proman_seller

logger = logging.getLogger(__name__)

# (nom, tavsif, narx so'm, [Uzum rasm ID lari]).
_PRODUCTS = [
    # ── Oshxona va maishiy texnika ──────────────────────────────────────────
    ("Mikroto'lqinli pech QLT MWS-2099-BL",
     "QLT MWS-2099-BL mikroto'lqinli pech — tez isitadi, muzdan tushiradi va "
     "qayta isitadi. Oson boshqaruv, oilaviy oshxona uchun qulay.",
     649000, ["d86369bsv8vo2t0frid0", "d4siahjtqdhua1ureq30", "d4siahgjsv1o95chej2g"]),

    ("Multivarka Redmond RMC-70, 5 litr, 49 dastur",
     "Redmond RMC-70 elektr multivarka — 5 litr, 49 ta dastur, 860 Vt. Palov, "
     "sho'rva, bug'da pishirish va shirinliklar bir qurilmada.",
     739030, ["cprv800sarnfdo992dig", "cg70dkvg49devoaae3pg", "chp2n7d6sfhndlbn1s50"]),

    ("Aerogril RAF air fryer, 1700 Vt, sensorli",
     "RAF air fryer — yog'siz sog'lom qovurish, 5/6.5/8 litr, oyna va sensorli "
     "boshqaruv bilan. Kartoshka, go'sht va sabzavot tabiiy mazada.",
     699000, ["d866qubsv8vo2t0fuaig", "d866qua1146tv071havg", "d866quc9g1ktqmlo1500"]),

    ("Changyutgich 3400 Vt, siklonli, HEPA filtr",
     "Kuchli 3400 Vt changyutgich — siklon tizimi, teleskopik quvur va HEPA "
     "filtr. Konteynerli, changsiz bo'shatiladi, uy uchun ideal.",
     749000, ["d8bu6nbsv8vo2t0hr030", "d8bu7k21146tv073dd80", "d755msi1146ojv9ac6k0"]),

    ("Go'sht maydalagich BOMA BM-389",
     "BOMA BM-389 elektr go'sht maydalagich — kuchli motor, revers funksiya. "
     "Go'sht, kolbasa va sabzavotni tez maydalaydi.",
     399000, ["d5tj50edd7ea4g2701qg", "d5tj50edd7ea4g2701pg", "d5tj50edd7ea4g2701q0"]),

    ("Planetar mikser BOMA BM-6004, 6 litr, 1500 Vt",
     "BOMA BM-6004 planetar mikser — 6 litrli idish, 1500 Vt. Xamir qorish, "
     "krem va bezak uchun oshxona kombayni.",
     957330, ["d7rjc53sv8vo2t0bimqg", "d7rjc521146tv06t5ugg", "d7rjc53sv8vo2t0bimr0"]),

    ("Kofe mashina UAKEEN, 20 bar, kapuchinatorli",
     "UAKEEN GERMANY avtomatik kofe mashinasi — 20 bar bosim, 1350 Vt, "
     "kapuchinator bilan. Uyda kafe darajasidagi espresso va latte.",
     1399000, ["d5ovld6ojia393mt2380", "d5ovlcuj76og35gjs3tg", "d5p6353q345softls3eg"]),

    ("Induksion elektr plita Bosch, sensorli",
     "Induksion elektr plita — sensorli, 4 rejimli, tez isitadi va energiya "
     "tejaydi. Uy va hovli oshxonasi uchun qulay.",
     355410, ["d64m6bedd7e7njq7t0eg", "d7lnenbsv8vo2t08vtf0", "d7gr6ma1146ojv9f8oe0"]),

    ("Aqlli havo namlagich, 4 litr, pultli",
     "Aqlli havo namlagich — 4 litr, pult, taymer, LED displey va 3 rejim. "
     "Xonadagi havoni yumshatadi, quruq havodan asraydi.",
     389000, ["d92keq49g1ku9j5fhjhg", "d92kf6s9g1ku9j5fhju0", "d92kghs9g1ku9j5fhktg"]),

    ("Shivaki SH-OH-1152 moyli isitgich, 11 seksiya",
     "Shivaki moyli isitgich — 11 seksiya, quritgich va ventilyator bilan. "
     "Xonani bir tekis isitadi, qishda uy uchun ishonchli.",
     550000, ["ctiq1jcopsf31vcr5tp0", "ctiq1osopsf31vcr5tsg"]),

    ("Havo sovutgich Elcom, iqlim kompleksi",
     "Elcom havo sovutgich va isitgich — sovutadi, namlaydi va tozalaydi. "
     "Yozgi issiqda konditsionerga tejamkor muqobil.",
     649000, ["d8mijai1146tv077demg", "d8mijabsv8vo2t0lqp10", "d8mijac9g1ktqmltu4eg"]),

    ("ARIZTON Classic elektr suv isitgich (boyler)",
     "ARIZTON Classic elektr suv isitgich — 30/50/80/100 litr. Uy uchun doimo "
     "issiq suv, ishonchli va tejamkor boyler.",
     810000, ["d8c2vijsv8vo2t0hte40", "d8c2vii1146tv073fro0", "d8c2vii1146tv073frng"]),

    # ── Parvarish va sog'liq ────────────────────────────────────────────────
    ("Fotoepilyator SAFORA, yuz va tana uchun",
     "SAFORA professional fotoepilyator — sovutish effekti bilan, yuz va tana "
     "uchun. Salon parvarishi endi uyning o'zida.",
     979110, ["d8r6o8k9g1ku9j5cbjh0", "d8r6odc9g1ku9j5cbjng", "d8r6oia1146phmqe6ia0"]),

    ("HYUNDAI XM-806 elektr tish cho'tkasi, IPX7",
     "HYUNDAI XM-806 tovushli elektr tish cho'tkasi — 5 rejim, IPX7 suvga "
     "chidamli, uchliklar bilan. Tishlarni chuqur va yumshoq tozalaydi.",
     329000, ["d90bnfc9g1ku9j5eep7g", "d8qeckq1146phmqdrktg", "d8qeckrsv8vnuj0v0k30"]),

    ("3D massajor, bo'yin va yelka, isitishli",
     "Simsiz 3D massajor — bo'yin va yelka uchun, isitish funksiyali, 2400 mAh. "
     "Kun oxiridagi charchoq va zo'riqishni yozadi.",
     239000, ["d8s30i49g1ku9j5cn4o0", "d8rejra1146phmqeas30", "d8rekt3sv8vnuj0vfv8g"]),

    # ── Smartfon, planshet va kompyuter ─────────────────────────────────────
    ("Planshet HONOR Pad X7, 8.7\", 90 Hz",
     "HONOR Pad X7 planshet — 8.7\" ekran, 90 Hz, 7020 mAh, Snapdragon 680. "
     "SIM va Wi-Fi bilan: o'qish, ish va ko'ngilochar uchun.",
     1499000, ["d4an1v5sp2tr82i45d70", "d4amottsp2tr82i45al0", "d4amp36j76ohd6e1eiag"]),

    ("Monitor Redmi 1A, 27\", IPS, 100 Hz",
     "Redmi 1A monitor — 27\", IPS, Full HD, 100 Hz. Uy, o'qish va ish uchun "
     "keng va aniq tasvir, ko'z charchamaydi.",
     1149000, ["d82tjsi1146tv07086r0", "d82tjtbsv8vo2t0elfi0", "d82tjubsv8vo2t0elfjg"]),

    ("Kolonka Canyon Hexagon 10, TWS, IPX5",
     "Canyon Hexagon 10 portativ Bluetooth kolonka — TWS juftlash, IPX5 suvdan "
     "himoya. Sayohat va davra uchun kuchli, toza ovoz.",
     391050, ["d8qdseq1146phmqdr9vg", "d8qdt3s9g1ku9j5c0d20", "d8qdtbi1146phmqdraj0"]),

    ("Hoco DI86 gaming to'plam, 4 tasi 1 da",
     "Hoco DI86 4-in-1 gaming to'plam — RGB mexanik klaviatura, quloqchin, "
     "sichqoncha va gilamcha. Kompyuterni to'liq jihozlaydi.",
     299900, ["d59k2sbtqdhjp1vd9eh0", "d59k4f3tqdhjp1vd9em0", "d59k3ors2tab83s94i8g"]),

    ("Printer Canon PIXMA G3430, rangli MFU, Wi-Fi",
     "Canon PIXMA G3430 — rangli printer-skaner-kopir, A4, Wi-Fi. Uy va ofis "
     "uchun tejamkor siyohli bosma, original.",
     1959000, ["d5oalb3q345softlg31g", "d5oalcuojia393mspu8g", "d5oalcjq345softlg330"]),

    # ── Avto va xavfsizlik ──────────────────────────────────────────────────
    ("Videoregistrator TEYES Q8 PRO, 3 kamera",
     "TEYES Q8 PRO videoregistrator — 3 kamera, Wi-Fi kuzatuv, tungi rejim. "
     "Avtomobil yo'lini to'liq va aniq yozib boradi.",
     559000, ["d8e6dtc9g1ktqmlqmugg", "d4lefumj76oneqanjmk0", "d4lefulsp2tr82i7m0qg"]),

    ("Wi-Fi IP kamera Tapo C210, 2K, buriluvchi",
     "TP-Link Tapo C210 — 2K aniqlikdagi ichki Wi-Fi kamera, 360° buriladi, "
     "tungi ko'rish. Uy va bolani telefondan kuzatib turing.",
     299000, ["d6dljqvqkmak8dt83a2g"]),

    ("Metall qulfli seyf, uy va ofis uchun",
     "Mustahkam metall seyf — kalitli qulf bilan. Pul, hujjat va qimmatbaho "
     "buyumlarni uy yoki ofisda ishonchli saqlaydi.",
     430000, ["d9a7qfi1146g73hsa2i0", "d9a7qf3sv8vsdeu8o2mg"]),

    # ── Oshxona texnikasi (davomi) ──────────────────────────────────────────
    ("Termopot HALEY HA680, 6.8 litr",
     "HALEY HA680 termopot — 6.8 litr, haroratni ushlab turadi. Kun bo'yi "
     "issiq suv tayyor: choy, qahva va nonushta uchun qulay.",
     280000, ["d8lp6qc9g1ktqmltj7tg", "d8lp6sbsv8vo2t0lfvi0", "d8lp6sc9g1ktqmltj7v0"]),

    ("Robot changyutgich Xiaomi Robot Vacuum S40",
     "Xiaomi Robot Vacuum S40 — 10000 Pa gacha so'rish, aqlli navigatsiya. "
     "Uyni o'zi tozalaydi, sizga vaqt bo'shatadi.",
     1999000, ["d9720ec9g1ku9j5hdri0", "d9720ejsv8vsdeu7blrg", "d1hqlu6ojia34bbvve9g"]),

    ("Gril ko'mirli AIKO, mangal-barbekyu, g'ildirakli",
     "AIKO ko'mirli gril — termometrli, g'ildirakli, ko'chma mangal-barbekyu. "
     "Hovli, dala va piknik uchun mazali kabob va grill.",
     769990, ["d8oiama1146tv0787f00", "d8oiamc9g1ktqmluoan0", "d8oiama1146tv0787evg"]),

    ("Muzlatgich Biryusa M412, ixcham, 80 litr",
     "Biryusa M412 ixcham muzlatgich — 80 litr. Talaba, ofis va kichik oila "
     "uchun ikkinchi muzlatgich sifatida qulay.",
     2699000, ["d82pe521146tv0704vvg", "d82pe6i1146tv0705010", "d82s6njsv8vo2t0ekh60"]),

    ("Kir yuvish mashinasi Ziffler avtomat, 6/8 kg",
     "Ziffler avtomat kir yuvish mashinasi — 6/8 kg, ko'p dasturli. Oila kiri "
     "uchun tejamkor va ishonchli yechim.",
     2699000, ["d97qvdi1146g73hraqv0", "d97qvdjsv8vsdeu7ooo0", "d97qnvrsv8vsdeu7ok90"]),

    ("Kir yuvish mashinasi Sirius Malyutka, 2 kg",
     "Sirius Malyutka mini kir yuvish mashinasi — 2 kg, ixcham va yengil. "
     "Ijara uy, dala hovli va tez yuvish uchun qulay.",
     519000, ["d3oekhr4eu2imglefet0", "d4jvcqdv2sjnqk4jclng", "d4jfqh6j76oneqamuuig"]),

    # ── Smartfon va noutbuk ─────────────────────────────────────────────────
    ("Smartfon OPPO A5i, 4+4/64 GB, 1 yil kafolat",
     "OPPO A5i smartfoni — (4+4) GB / 64 GB, quvvatli batareya. Kundalik "
     "foydalanish uchun ishonchli, 1 yil kafolat bilan.",
     1850000, ["d6ilaajvgbktbpvmur8g", "d6ilaajvgbktbpvmur7g", "d6ilaai1146k64hudh3g"]),

    ("Noutbuk HP 250 G7, i3, 8/256 GB, 15.6\" FHD",
     "HP 250 G7 noutbuk — Intel Core i3, 8 GB RAM, 256 GB SSD, 15.6\" Full HD, "
     "Windows. Ish va o'qish uchun ishonchli hamroh.",
     4249000, ["d9jf92bsv8vsdeucu250", "d9b2b3bsv8vsdeu96a80", "d9b2b3a1146g73hso220"]),

    ("Kuchlanish stabilizatori GIDROX GDC 2000VA",
     "GIDROX GDC 2000VA stabilizator — releli, 220 V. Kuchlanish sakrashidan "
     "muzlatgich, televizor va texnikani himoya qiladi.",
     541750, ["d8sh2ra1146phmqemr80", "d8sh2rc9g1ku9j5crti0", "cn8d85h25kub33f43cc0"]),

    ("Gaming quloqchin 2E GAMING HG315, 7.1",
     "2E GAMING HG315 simli o'yin quloqchini — 7.1 tovush, USB, RGB. Kuchli "
     "bas va aniq ovoz: o'yin va onlayn muloqot uchun.",
     266310, ["d66nml3vv0v6ikl3p4f0", "d66nml3q345uoeq1vvh0", "d66nml5sp2tk1m7i3qdg"]),

    ("Non pishirgich (xlebopechka), 19 dastur, 800 Vt",
     "Aqlli non pishirgich — xamir qoradi va nonni o'zi yopadi, 19 ta dastur, "
     "800 Vt. Uyda har kuni yangi, mazali non.",
     999990, ["cvj2dj6i4n36ls4194q0", "cvj2dkdpb7f9qcnjvgc0", "cvj2dlbvgbkm5ehmcr10"]),

    ("Kvadrokopter M9 Pioner, mini drone, LED",
     "M9 Pioner mini kvadrokopter — masofadan boshqariladi, 360° aylanish va "
     "LED chiroq. Bolalar va kattalar uchun qiziqarli sovg'a.",
     504100, ["d8g2h221146tv074t8og"]),

    ("Havo tozalagich ARTEL AP151, HEPA + ko'mir",
     "ARTEL AP151 havo tozalagich va namlagich — NanoCloud texnologiyasi, HEPA "
     "va ko'mir filtr. Chang, allergen va hiddan toza havo.",
     1199000, ["d6bubvlv2sjhfufigvfg", "d4g587dsp2tr82i5t770", "d65j22rvv0v6ikl39mqg"]),

    ("Elektr ustara Wahl Super Close Shaver",
     "Wahl Super Close professional elektr ustara — silliq va toza soqol "
     "olish uchun. Ishonchli original brend.",
     572000, ["ch6ir9nhj8j2b6b6l99g", "ch6ir9h6i6dvgfec2gfg", "ch6ir9h6i6dvgfec2gg0"]),

    # ── Asbob-uskuna ────────────────────────────────────────────────────────
    ("Akkumulyatorli drel-shurupovert 48V, keys bilan",
     "Cho'tkasiz akkumulyatorli drel-shurupovert 48V — 2 ta Li-ion batareya, "
     "zarbli rejim, chamadonda. Uy ustaligi uchun kuchli to'plam.",
     209990, ["d85bdh21146tv07149l0", "d5fn920jsv1neactdr9g", "d5fn923tqdhjp1velgp0"]),

    ("MAGNAT yuqori bosimli yuvish mashinasi (moyka)",
     "MAGNAT professional yuqori bosimli moyka — avtomobil, hovli va devorni "
     "kuchli suv oqimi bilan tez tozalaydi.",
     643490, ["d91uhfc9g1ku9j5f73h0", "d8vou8jsv8vnuj117gl0", "d8voucrsv8vnuj117go0"]),

    ("Benzin generator GIDROX GD-3900, 3 kVt, 220 V",
     "GIDROX GD-3900 benzin generatori — 3 kVt, 220 V, 15 litrli bak. Chiroq "
     "o'chganda uy, do'kon va asboblarni quvvat bilan ta'minlaydi.",
     3120000, ["cv8ka0ui4n36ls3uchh0", "d89ii6bsv8vo2t0h7e0g", "d89ii6c9g1ktqmlpa4c0"]),

    ("Mini pech ODUL-1010, 36 litr, elektr duxovka",
     "ODUL-1010 mini elektr duxovka — 36 litr, gril rejimi bilan. Pishiriq, "
     "go'sht va sabzavotni uyda tez tayyorlaydi. 3 yil kafolat.",
     658350, ["d6asa41e6ph7gqpj4lq0", "d6asa4pe6ph7gqpj4ls0", "d6asa61e6ph7gqpj4ltg"]),

    # ── TV, proyektor va audio ──────────────────────────────────────────────
    ("Televizor TCL V6C 50\", 4K UHD, Google TV",
     "TCL V6C Smart TV — 50\", 4K UHD, Google TV, HDR10, Bluetooth 5.2. "
     "Sevimli filmlar va YouTube katta ekranda, jonli ranglarda.",
     3439000, ["d8vr8q3sv8vnuj1197i0", "d8vr8q49g1ku9j5e99mg", "d8vr8q21146phmqg4390"]),

    ("Smart proyektor HY300 PRO, Android, Wi-Fi",
     "HY300 PRO aqlli proyektor — Android, Wi-Fi, uy kinoteatri. Devor yoki "
     "pardaga katta ekranli kino va multfilm ko'rsatadi.",
     379000, ["d9j2aa3sv8vsdeucqlp0", "d9j29q3sv8vsdeucqlc0", "d9j29pk9g1ku9j5mt7c0"]),

    ("Raqamli foto kamera Campus 50MP HD, Wi-Fi",
     "Campus Portable 50MP foto kamera — 1080P video, 8x zoom, avtofokus, "
     "Wi-Fi. Sayohat va oilaviy lahzalarni yorqin saqlang.",
     309900, ["d8bvrus9g1ktqmlpukq0", "d8bvq4k9g1ktqmlpujm0", "d8bvq7rsv8vo2t0hroc0"]),

    ("Xiaomi Redmi TV Saundbar MDZ-34-DA, Bluetooth",
     "Xiaomi Redmi TV saundbar — Bluetooth, televizor va kompyuter uchun kuchli "
     "stereo ovoz. Kino va musiqa kinoteatr sifatida yangraydi.",
     649000, ["d94ae0s9g1ku9j5g7hdg", "d94ae4c9g1ku9j5g7heg", "cuif5ak5j42bjc4cpvag"]),

    ("Kondensatorli studiya mikrofoni, kronshteyn + pop-filtr",
     "Kondensatorli USB mikrofon — RGB yoritgich, kronshteyn va pop-filtr "
     "bilan. Blog, strim va ovoz yozish uchun toza studiya sifati.",
     449000, ["d7u8pr21146tv06uasgg", "d7u8q049g1ktqmlkr06g", "d7u8q0rsv8vo2t0cns30"]),

    # ── Uy va oshxona (davomi) ──────────────────────────────────────────────
    ("Oshxona dudboroni (vityajka) Vitech Flora, 60 sm",
     "Vitech Flora osma oshxona dudboroni — 60 sm, kuchli havo tortadi. "
     "Oshxonadagi is, tutun va yog' hidini tez chiqaradi.",
     499000, ["d8lu54i1146tv0775ii0", "d8lu53rsv8vo2t0lishg", "d8lu53s9g1ktqmltm440"]),

    ("Hofmann 1500W immersion (qo'l) blender to'plami",
     "Hofmann 1500 Vt immersion blender — 3 ta model to'plami. Sho'rva, smuzi "
     "va sabzavotni to'g'ridan-to'g'ri idishda maydalaydi.",
     755000, ["d6vc4q21146ojv984l30", "d6vc4qs3obpjedc36peg", "d6vc4rc3obpjedc36pf0"]),

    ("Payvandlash invertori ZX7-300, 300A, MMA",
     "ZX7-300 inverter payvandlash apparati — 300A, MMA, professional. Uy "
     "ustaligi va temir ishlari uchun kuchli va barqaror.",
     499000, ["d76a8vbsv8vlb6mkpekg", "d751r8jsv8vlb6mk8ibg", "d751r8a1146ojv9a9n7g"]),

    ("Perforator professional, 800 Vt, SDS PLUS, keys",
     "Professional perforator — 3 rejimli, 800 Vt, 26 mm, SDS PLUS patron, "
     "mustahkam keysda. Beton, g'isht va devor teshish uchun.",
     349000, ["d918dd3sv8vnuj11t660", "d917u8i1146phmqgnpng", "d5kh3bjtqdhu87jscrs0"]),

    ("Bolgarka (burchak silliqlash), 180 mm",
     "Sozlanuvchi bolgarka — 180 mm, burchakli silliqlash mashinasi. Metall "
     "kesish, silliqlash va tozalash ishlari uchun kuchli asbob.",
     379000, ["d66uu71e6ph7gqphburg", "d66uu71e6ph7gqphbus0", "d66uu77qkmalqfnb0hkg"]),

    ("Suv nasosi avtomat Alfa Grand, 100% mis",
     "Alfa Grand avtomatik suv nasosi — 100% mis o'ram, quruq ishlashdan "
     "himoya. Uy va bog'ga barqaror suv bosimi beradi.",
     559990, ["d5rocqr4eu2jdglgl830", "d5rocrr4eu2jdglgl83g", "d5rocsviub393sddhe00"]),

    ("Giroskuter, 7 dyumli",
     "7 dyumli giroskuter — muvozanatli, yorqin g'ildirakli. Bolalar va "
     "o'smirlar uchun qiziqarli va zamonaviy transport.",
     1080000, ["ctrmjec5j42bjc4686gg", "cs2k9d3i153t30uotb10", "ctrmjflht56ksubbd0p0"]),

    ("Bog' uchun akkumulyatorli o't o'roq Biyoti BYT-BC53",
     "Biyoti BYT-BC53 akkumulyatorli o't o'roq (trimmer) — simsiz, yengil. "
     "Hovli va bog'dagi o'tni tez va oson o'radi.",
     335000, ["d7s6npi1146tv06td3o0", "d7s3f33sv8vo2t0bnnn0", "d10idn33uvpglcmamjq0"]),

    ("Katta powerbank 50000-160000 mAh, tezkor",
     "Katta sig'imli tashqi akkumulyator — 50000-160000 mA/soat, tezkor "
     "quvvatlash. Uzoq safar va sayohatda telefon quvvatsiz qolmaydi.",
     457380, ["ctpr64k5j42bjc460q30", "ctpr655ht56ksubb5m00", "ctpr64k5j42bjc460q3g"]),

    ("Dazmol POLARIS PIR 2497AK, bug'li",
     "POLARIS PIR 2497AK bug'li dazmol — kuchli bug', 3 m shnur. Kiyimni tez "
     "va silliq dazmollaydi, kundalik foydalanish uchun qulay.",
     619000, ["d290h1d2lln1rmfjjprg", "d290h1viub3br3215sb0", "d290h252lln1rmfjjpsg"]),

    ("Lyustra LED ventilyator, pultli, 30 m² gacha",
     "LED ventilyatorli lyustra — pultli, 3 rejim yoritish, 6 tezlik, taymer, "
     "30 m² gacha. Yoritish va salqinlik bir qurilmada.",
     1950300, ["d7tiu03sv8vo2t0ce9g0", "d7titsa1146tv06u1a10", "d7tiu1a1146tv06u1a5g"]),

    ("Oshxona kombayni, 4 tasi 1 da",
     "Oshxona kombayni — sharbat siqqich, blender, maydalagich va qahva "
     "maydalagich bir qurilmada. Oshxona ishini bir necha barobar tezlashtiradi.",
     615000, ["d4g0496j76ooegrm7teg", "d0gqj7q7s4fo7mq8rotg", "d0gqjab3uvph509tp2pg"]),

    ("Kir quritgich Nika, yig'iladigan, 20 m",
     "Nika polga o'rnatiladigan kir quritgich — yig'iladigan metall, 20 m "
     "ip. Ko'p kirni bir joyda quritadi, joy tejaydi.",
     419000, ["csnqakjvgbkpg1nlch70", "csnqamjvgbkpg1nlch80", "csnqao5pq3ggq63cceug"]),

    ("Homix soch quritgich (fen), 1600 Vt, ionizatsiya",
     "Homix fen — yuqori tezlik 110000 ayl/min, 1600 Vt, ionizatsiya va "
     "bolalar rejimi. Sochni tez quritadi va jonli ko'rsatadi.",
     359000, ["d9ae17i1146g73hsf1i0", "d6n3s921146th72tpa4g", "d4csvu5v2sjnqk4h1kvg"]),
]


def seed_proman_top2() -> int:
    """Uzum'dan saralangan 2-partiya 60 mahsulotni ProMan do'koniga qo'shadi."""
    return seed_products(_PRODUCTS, _find_proman_seller, "ProMan Top-60 (2-partiya)")
