"""
Run this script after every `qlik get` to restore the preceding LOAD in 1___SUB.qvs.
Usage: python _add_preceding_load_products.py
"""
import os

file = os.path.join(os.path.dirname(__file__), '1___SUB.qvs')

with open(file, 'rb') as f:
    content = f.read()

if b'    LOAD' in content:
    print('Preceding LOAD already present, nothing to do.')
    exit(0)

fields = [
    ('"product_hash_id"',                           '%ProductHashID'),
    ('"product_group_hash_id"',                     '%ProductGroupHashID'),
    ('"product_attribute_hash_id"',                 '%ProductAttributeHashID'),
    ('"product_id"',                                'ProductID'),
    ('"product_lob_sku"',                           'ProductLobSKU'),
    ('"product_group_lob_sku"',                     'ProductGroupLobSKU'),
    ('"product_name"',                              'ProductName'),
    ('"product_format_old"',                        'ProductFormatOld'),
    ('"product_strength_old"',                      'ProductStrengthOld'),
    ('"product_nicotine_strenth"',                  'ProductNicotineStrenth'),
    ('"product_portion_type"',                      'ProductPortionType'),
    ('"product_price_segment"',                     'ProductPriceSegment'),
    ('"product_type_original"',                     'ProductTypeOriginal'),
    ('"product_pg_artnr"',                          'ProductPgArtnr'),
    ('"product_flavour"',                           'ProductFlavour'),
    ('"product_manufacturer_old"',                  'ProductManufacturerOld'),
    ('"product_type_old"',                          'ProductTypeOld'),
    ('"product_brand_old"',                         'ProductBrandOld'),
    ('"product_data_source"',                       'ProductDataSource'),
    ('"product_brand_url"',                         'ProductBrandUrl'),
    ('"product_image_url"',                         'ProductImageUrl'),
    ('"product_insight_price_segment"',             None),              # kept snake_case
    ('"product_price_segment_swedish_match"',       None),              # kept snake_case
    ('"product_strength_mg"',                       'ProductStrengthMg'),
    ('"product_sub_category"',                      'ProductSubCategory'),
    ('"product_is_sample"',                         'ProductIsSample'),
    ('"product_type_group"',                        'ProductTypeGroup'),
    ('"product_type_group_desc"',                   'ProductTypeGroupDesc'),
    ('"product_culture"',                           'ProductCulture'),
    ('"product_stats_cans"',                        'ProductStatsCans'),
    ('"product_show_in_qlik_flag"',                 'ProductShowInQlik_Flag'),
    ('"product_is_sample_flag"',                    'ProductIsSample_Flag'),
    ('"product_in_qlik_flag"',                      'ProductInQlik_Flag'),
    ('"product_name_hash_id"',                      '%ProductNameHashID'),
    ('"product_created_date"',                      'ProductCreatedDate'),
    ('"product_created_year_month"',                'ProductCreatedYearMonth'),
    ('"product_nicotine_content_mg_per_pouch"',     'ProductNicotineContentMgPerPouch'),
    ('"product_brand_insights_pim"',                'ProductBrandInsightsPIM'),
    ('"product_manufacturer_insights_pim"',         'ProductManufacturerInsightsPIM'),
    ('"product_strength_pim"',                      'ProductStrengthPIM'),
    ('"product_format_pim"',                        'ProductFormatPIM'),
    ('"product_primary_flavor"',                    'ProductPrimaryFlavor'),
    ('"product_primary_flavor_sub_group"',          'ProductPrimaryFlavorSubGroup'),
    ('"product_primary_flavor_group"',              'ProductPrimaryFlavorGroup'),
    ('"product_secondary_flavor"',                  'ProductSecondaryFlavor'),
    ('"product_secondary_flavor_sub_group"',        'ProductSecondaryFlavorSubGroup'),
    ('"product_secondary_flavor_group"',            'ProductSecondaryFlavorGroup'),
    ('"product_flavor_type"',                       'ProductFlavorType'),
    ('"product_flavour_group_concat"',              'ProductFlavourGroupConcat'),
    ('"product_flavour_sub_group_concat"',          'ProductFlavourSubGroupConcat'),
    ('"product_flavour_concat"',                    'ProductFlavourConcat'),
    ('"product_flavour_is_fusion"',                 'ProductFlavourIsFusion'),
    ('"product_single_flavour_simple"',             'ProductSingleFlavourSimple'),
    ('"product_single_flavour_full"',               'ProductSingleFlavourFull'),
    ('"product_nicotine_type"',                     'ProductNicotineType'),
    ('"product_caffeine_content"',                  'ProductCaffeineContent'),
    ('"product_strength_insights_pim"',             'ProductStrengthInsightsPim'),
    ('"product_type_insights_pim"',                 'ProductTypeInsightsPim'),
    ('"product_format_insights_pim"',               'ProductFormatInsightsPim'),
    ('"product_contains_caffeine_flag"',            'ProductContainsCaffeine_Flag'),
    ('"product_contains_tobacco_flag"',             'ProductContainsTobacco_Flag'),
    ('"product_type"',                              'ProductType'),
    ('"product_is_nicotine_pouche_flag"',           'ProductIsNicotinePouche_Flag'),
    ('"product_is_tobacco_free_flag"',              'ProductIsTobaccoFree_Flag'),
    ('"product_is_vape_flag"',                      'ProductIsVape_Flag'),
    ('"product_is_section_access_addon_flag"',      'ProductIsSectionAccessAddon_Flag'),
    ('"product_single_flavour_simple_pt"',          'ProductSingleFlavourSimplePT'),
    ('"product_name_with_stats_cans_hash_id"',      '%ProductNameWithStatsCansHashID'),
    ('"product_tobacco_type"',                      'ProductTobaccoType'),
    ('"product_strength"',                          'ProductStrength'),
    ('"product_brand"',                             'ProductBrand'),
    ('"product_manufacturer"',                      'ProductManufacturer'),
    ('"product_format"',                            'ProductFormat'),
    ('"product_strength_pt"',                       'ProductStrengthPT'),
    ('"product_format_pt"',                         'ProductFormatPT'),
    ('"product_flavour_pt"',                        'ProductFlavourPT'),
    ('"product_insight_price_segment"',             'ProductInsightPriceSegment'),
    ('"product_price_segment_swedish_match"',       'ProductPriceSegmentSwedishMatch'),
    ('NULL()',                                       'ProductPrimaryAndSecondaryFlavour'),
]

lines = []
for i, (src, alias) in enumerate(fields):
    comma = ',' if i < len(fields) - 1 else ''
    if alias is None:
        lines.append(f'        {src}{comma}')
    else:
        lines.append(f'        {src:<46} as {alias}{comma}')

load_block = '    LOAD\r' + '\r'.join(lines) + '\r    ;\r'

old = b';\r\r    SELECT \r'
new = b';\r\r    Products:\r' + load_block.encode('utf-8') + b'    SELECT \r'

if old not in content:
    print('ERROR: Could not find the expected pattern in the file.')
    print('The file may have changed. Check manually.')
else:
    content = content.replace(old, new)
    with open(file, 'wb') as f:
        f.write(content)
    print('Done. Preceding LOAD added successfully.')
