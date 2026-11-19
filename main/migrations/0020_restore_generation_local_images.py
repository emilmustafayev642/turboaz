from django.db import migrations


IMAGE_PATHS = {
    'generations/qw6ykj1dif4knpwvsy5q': 'generations/generations/2018-amg-line.webp',
    'generations/pjfe8oyd6panpvp8uybv': 'generations/generations/images_2.webp',
    'generations/jftqgx8raof6isrurzf8': 'generations/generations/BMW-5-f10-2.webp',
    'generations/l1lcvs5opftfaomosxek': 'generations/generations/images_3.webp',
    'generations/g71vhehmxsw8btadopcc': 'generations/generations/bmw-5-series-2023-2025-1720458650.8683367.webp',
    'generations/ulx78rx7gyyfijrnmmja': 'generations/generations/images_4.webp',
    'generations/zowoheye8w60xuxvmfbz': 'generations/generations/images_5.webp',
    'generations/hpgzuo1wte7wbeq2moy1': 'generations/generations/Isuzu-NPR66L-Steel-Tipper_5.webp',
    'generations/cb54oleyorbmjx05kpzv': 'generations/generations/W211.webp',
    'generations/vwntzykpmq9hkxbkdive': 'generations/mercedes-benz_e-class_833797.webp',
    'generations/olbxxyn6h52zcinzfi7v': 'generations/generations/E-Class.webp',
    'generations/ru4gfrzxvjz1slxolkrm': 'generations/generations/images_7.webp',
    'generations/xb7uxp4f6bjjgvuuxj25': 'generations/large.webp',
    'generations/ke4vhitwiktfkex2ok1u': 'generations/original.webp',
    'generations/l99cgx1h9uqrk2ppbi60': 'generations/59539247.webp',
    'generations/hgrw15szbs0y4ni9x79o': 'generations/toyota-camry-xv70.webp',
    'generations/eltffremrgaaveldnijp': 'generations/generations/kia_sorento_2-567x425.webp',
    'generations/u23qv3783nneb6ju8hml': 'generations/500x_kia_sorento_g8108.webp',
    'generations/jl3sftslw3ibtiaooeeu': 'generations/generations/images_8.webp',
    'generations/dwk9wywcdub6skyrzgcz': 'generations/1_l.webp',
    'generations/pyowjh30wu7m60ietydf': 'generations/generations/1714506338-2018_yam_mt07_eu_mnm3dsj_stu_001_03-55857.webp',
    'generations/bqz81soldqtwap4z29f4': 'generations/generations/hyundai-santa-fe-2000-2006-1681479455.9841316.webp',
    'generations/eknb8zcr1379u5si3vw1': 'generations/generations/images_9.webp',
    'generations/butb55r3tvzyfxfzactx': 'generations/generations/images_10.webp',
    'generations/gdgpgrq2fnuwobhgndkb': 'generations/generations/362.webp',
    'generations/rdc2efyy44qlj0qoykac': 'generations/porsche-cayenne-958-48-turbo-2010-umbra-braun-metallic.webp',
    'generations/egjqujfl0f9hcwkx1wia': 'generations/generations/2026-porsche-cayenne-1920x800.webp',
    'generations/yze51jcddyz6um8y1q6z': 'generations/generations/1627926341_bmw-x5-2006-2010-2.webp',
    'generations/eo2bcyefyjjfmhds99xl': 'generations/bmw_x5_879785.webp',
    'generations/bfmlzv0pdfytug3fgerj': 'generations/generations/1400x936.webp',
    'generations/lt4bou6uztzqdwmrfhwr': 'generations/generations/BMW-X6-2.webp',
    'generations/flmipr6hfg4vpcr5yfa2': 'generations/generations/images_11.webp',
    'generations/uely28gqw0vc31c01jxk': 'generations/bmw-x6-g06-facelift-upgrade-review-italy.webp',
    'generations/f1zdxjhs5lhhgnefncn3': 'generations/mercedes-benz-s-class-w221-2005-2013.webp',
    'generations/vre4giaqbmbk4cmrx2rc': 'generations/generations/mercedes.webp',
    'generations/pccvb999morigmjlcmpf': 'generations/generations/mercedes-s-class-2020-2026-1779446023.6677816.webp',
    'generations/le5apgnxa0qogezmifsd': 'generations/generations/BMW_740d_F01_front_20100724.webp',
    'generations/jlw79j5pqr9qeihvm7qw': 'generations/bmw-7-series-g11-g12-2015-2022.webp',
    'generations/prs6ux58fnkla3i8zb7w': 'generations/generations/bmw_7-series_1337499.webp',
    'generations/njeo4exiyppzmzltqi1t': 'generations/generations/images_12.webp',
    'generations/ewocdmdsh32txfmethcu': 'generations/generations/1.webp',
    'generations/ux55yee5kfkwfmqncp83': 'generations/2.webp',
    'generations/tzpgghv1s1ejqh4qaq1a': 'generations/generations/images_13.webp',
    'generations/apbjwzxjasuciokzspvx': 'generations/generations/4.webp',
    'generations/kq0uqhykzf6bbmizobri': 'generations/generations/5.webp',
    'generations/bqrxcramtf5mkztlcyz5': 'generations/5.webp',
    'generations/xu2idrj25syc44wyplbv': 'generations/generations/images_14.webp',
    'generations/s1rkbyrnlzoerbvcdxmb': 'generations/generations/20637561.webp',
    'generations/gdrk4mdbf7eq7s8gfcwf': 'generations/360.webp',
    'generations/xui5h87f4c9p6q7f8zqd': 'generations/17.webp',
    'generations/ooqmt2nk55vkqfrvwwin': 'generations/generations/18.webp',
    'generations/zr8k6ofodvlt2ihcycej': 'generations/generations/19.webp',
    'generations/jmc8sm5nsodh42r2vhx1': 'generations/generations/images_15.webp',
    'generations/prq95mkvns1fa0pqufa7': 'generations/20.webp',
    'generations/im7obemkq2ajlsf8dl0x': 'generations/generations/images_17.webp',
    'generations/fwr0c14yopzdgtou7hkd': 'generations/generations/images_18.webp',
    'generations/hu1ldtrij7uht618v6jk': 'generations/generations/images_19.webp',
    'generations/mjrxkgbjyak24mx1xmp1': 'generations/21.webp',
    'generations/vqubjuegalrakcf5xlp6': 'generations/generations/images_20.webp',
    'generations/acs95iunqtmtk70p3oa8': 'generations/generations/23.webp',
    'generations/awqc3nqylbj4hziesbsu': 'generations/generations/images_21.webp',
    'generations/iif6adjvwgis2vv7wlz5': 'generations/generations/24.webp',
    'generations/kdwkbm0k8jh2htzdwyud': 'generations/generations/26.webp',
    'generations/dqwftkrzrbirpovglu6u': 'generations/generations/25.webp',
    'generations/yb2mk3mclbecnsphu6v1': 'generations/generations/images_22.webp',
    'generations/m3oulluicleciqhoordd': 'generations/generations/images_23.webp',
    'generations/wjmxnmmkgjjldlvsfzhq': 'generations/generations/images_24.webp',
    'generations/urntxyf4jmhdegzkazau': 'generations/generations/images_25.webp',
    'generations/gdajvtnvc10yketxq1p6': 'generations/generations/27.webp',
    'generations/g9z7teljqfikvxfgybp4': 'generations/28.webp',
    'generations/jyofjbicmeeeoa9obvp5': 'generations/29.webp',
    'generations/fewnrsv8f4mpr71ceyk6': 'generations/30.webp',
    'generations/ycopwiq6vtxtghzxqzjm': 'generations/generations/images_26.webp',
    'generations/mytraweipaswwwjtwjoe': 'generations/generations/images_27.webp',
    'generations/lm5jcswkbpbupkk7bzf5': 'generations/generations/images_28.webp',
    'generations/id4bngcqtwj56pnnklif': 'generations/generations/images_29.webp',
    'generations/qydpdqobb2tv75h9llaq': 'generations/generations/30.webp',
    'generations/o9yof4e6imlpdow252co': 'generations/generations/31.webp',
    'generations/bwaqr2vrvbsznimalyix': 'generations/generations/images_30.webp',
    'generations/drskx2ldnycgvjqzonvp': 'generations/generations/32.webp',
    'generations/piogs4yr34jzz0sdo1ge': 'generations/33.webp',
    'generations/hfottisfxiu7ybuvf0q7': 'generations/generations/images_31.webp',
    'generations/nq5eqnypt0gkortcgkft': 'generations/generations/images_32.webp',
    'generations/nvs1attaorcfds0gw5mz': 'generations/3.webp',
}


def update_generation_images(apps, schema_editor, paths):
    CarGeneration = apps.get_model('main', 'CarGeneration')
    database = schema_editor.connection.alias

    for old_path, new_path in paths.items():
        CarGeneration.objects.using(database).filter(image=old_path).update(image=new_path)


def restore_local_images(apps, schema_editor):
    update_generation_images(apps, schema_editor, IMAGE_PATHS)


def restore_previous_images(apps, schema_editor):
    update_generation_images(
        apps,
        schema_editor,
        {local_path: old_path for old_path, local_path in IMAGE_PATHS.items()},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_listing_delete_reason_listing_deleted_at_and_more'),
    ]

    operations = [
        migrations.RunPython(restore_local_images, restore_previous_images),
    ]
