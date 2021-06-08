def new_xml_file_content(rok, miesiac, sprzedaz, k19_k20_lst):
    return """<?xml version="1.0" encoding="utf-8"?>
    <JPK xmlns:etd="http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://crd.gov.pl/wzor/2020/05/08/9393/ http://crd.gov.pl/wzor/2020/05/08/9393/schemat.xsd" xmlns="http://crd.gov.pl/wzor/2020/05/08/9393/">
      <Naglowek>
        <KodFormularza kodSystemowy="JPK_V7M (1)" wersjaSchemy="1-2E">JPK_VAT</KodFormularza>
        <WariantFormularza>1</WariantFormularza>
        <DataWytworzeniaJPK>2021-05-23T13:15:25.3978911</DataWytworzeniaJPK>
        <NazwaSystemu>Formularz uproszczony</NazwaSystemu>
        <CelZlozenia poz="P_7">1</CelZlozenia>
        <KodUrzedu>2550</KodUrzedu>
        <Rok>""" + str(rok) + """</Rok>
        <Miesiac>""" + str(miesiac) + """</Miesiac>
      </Naglowek>
      <Podmiot1 rola="Podatnik">
        <OsobaFizyczna>
          <etd:NIP>1234567890</etd:NIP>
          <etd:ImiePierwsze>JAN</etd:ImiePierwsze>
          <etd:Nazwisko>NOWAK</etd:Nazwisko>
          <etd:DataUrodzenia>1970-01-31</etd:DataUrodzenia>
          <Email>jannowak@onet.pl</Email>
          <Telefon>888333444</Telefon>
        </OsobaFizyczna>
      </Podmiot1>
      <Deklaracja>
        <Naglowek>
          <KodFormularzaDekl kodSystemowy="VAT-7 (21)" kodPodatku="VAT" rodzajZobowiazania="Z" wersjaSchemy="1-2E">VAT-7</KodFormularzaDekl>
          <WariantFormularzaDekl>21</WariantFormularzaDekl>
        </Naglowek>
        <PozycjeSzczegolowe>
          <P_19>""" + str(k19_k20_lst[0]) + """</P_19>
          <P_20>""" + str(k19_k20_lst[1]) + """</P_20>
          <P_37>""" + str(k19_k20_lst[0]) + """</P_37>
          <P_38>""" + str(k19_k20_lst[1]) + """</P_38>
          <P_42>0</P_42>
          <P_43>0</P_43>
          <P_48>0</P_48>
          <P_51>""" + str(k19_k20_lst[1]) + """</P_51>
          <P_68>0</P_68>
          <P_69>0</P_69>
        </PozycjeSzczegolowe>
        <Pouczenia>1</Pouczenia>
      </Deklaracja>
      <Ewidencja>
        """ + sprzedaz + """
        <SprzedazCtrl>
          <LiczbaWierszySprzedazy>0</LiczbaWierszySprzedazy>
          <PodatekNalezny>0</PodatekNalezny>
        </SprzedazCtrl>
        
        <ZakupCtrl>
          <LiczbaWierszyZakupow>0</LiczbaWierszyZakupow>
          <PodatekNaliczony>0</PodatekNaliczony>
        </ZakupCtrl>
      </Ewidencja>
    </JPK>
    """

# Liczba wierszy sprzedaży i podatek należny od sprzedaży może być "0", bo jest aktualizowane automatycznie
# W tym pliku podane są dane przykładowe, ponieważ w zamyśle tworzony był dla jednego podmiotu.
# W razie potrzeby można dodać w GUI opcję edycji danych do plików XML.
