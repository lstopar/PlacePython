import sys
import csv
import traceback
from datetime import datetime

OUT_FIELDS = [
    'id',
    'cas',
    'ministry_id',
    'ministry_desc',
    'delovno_mesto',
    'delovno_mesto_desc',
    'placilni_razred',
    'placa',
    'razlika_minimalec',
    'stevilo_dodatkov_pos',
    'vsota_dodatkov_pos',
    'stevilo_dodatkov_neg',
    'vsota_dodatkov_neg',
    'stevilo_bonusov_pos',
    'vsota_bonusov_pos',
    'stevilo_bonusov_neg',
    'vsota_bonusov_neg'
]

ACCESORY_COLS = [   # dodatki
    'polozajni_dodatek_c010bruto',
    'polozajni_dodatek_c011bruto',
    'polozajni_dodatek_c012bruto',
    'dodatek_za_delovno_dobo_c020bruto',
    'dodatek_za_delovno_dobo_za_ju_c021bruto',
    'dodatek_mentorstvo_c030bruto',
    'dodatek_mag_dr_c040bruto',
    'dodatek_dvojezicnost_c050bruto',
    'dodatek_dvojezicnost_c051bruto',
    'dodatek_dvojezicnost_c052bruto',
    'dodatek_ionizirajoce_sevanje_c060bruto',
    'dodatek_citostatiki_c061bruto',
    'dodatek_kuzni_odpadki_c062bruto',
    'dodatek_nevarnost_c070bruto',
    'dodatek_izmensko_delo_c080bruto',
    'dodatek_deljeni_del_cas_c090bruto',
    'dodatek_delo_ponoci_c100bruto',
    'dodatek_delo_v_nedeljo_c110bruto',
    'dodatek_dela_prost_dan_c111bruto',
    'dodatek_dela_prost_dan_c112bruto',
    'dodatek_delo_prek_polnega_casa_c120bruto',
    'dodatek_stalna_pripravljenost_c130bruto',
    'dodatek_pripravljenost_na_domu_c140bruto',
    'dodatek_za_stalnost_c150bruto',
    'dodatek_povecan_obseg_dela_c160bruto',
    'dodatek_povecan_obseg_dela_c170bruto',
    'dodatek_posebne_obremenitve_c180bruto',
    'dodatek_neenakomerno_razporejen_delovni_cas_c190bruto',
    'dodatek_neenakomerno_razporejen_delovni_cas_c191bruto',
    'dodatek_specialna_enota_c200bruto',
    'dodatek_specialna_enota_c201bruto',
    'dodatek_za_potapljanje_c202bruto',
    'dodatek_za_potapljanje_intervencija_c203bruto',
    'dodatek_poucevanje_3_predmetov_c204bruto',
    'dodatek_razrednistvo_c205bruto',
    'dodatek_razrednistvo_c206bruto',
    'dodatek_vrtci_c207bruto',
    'dodatek_vrtci_c208bruto',
    'dodatek_bolnisnicni_oddelek_c209bruto',
    'dodatek_prilagojeni_program_c210bruto',
    'dodatek_prilagojeni_program_c211bruto',
    'dodatek_prilagojeni_program_c212bruto',
    'dodatek_prilagojeni_program_c213bruto',
    'dodatek_prilagojeni_program_c214bruto',
    'dodatek_delo_z_osebami_z_motnjo_c215bruto',
    'dodatek_delo_z_osebami_z_motnjo_c216bruto',
    'dodatek_delo_z_osebami_z_motnjo_c217bruto',
    'dodatek_delo_z_osebami_z_motnjo_c218bruto',
    'dodatek_visina_2_4_m_c219bruto',
    'dodatek_visina_4_20_m_c220bruto',
    'dodatek_visina_nad_20_m_c221bruto',
    'dodatek_globina_c222bruto',
    'dodatek_tvegane_razmere_c223bruto',
    'dodatek_helikopter_c224bruto',
    'dodatek_delo_z_osebami_z_motnjo_nadzor_c225bruto',
    'dodatek_ogled_kd_c300bruto',
    'polozajni_dodatek_pravosodje_c301bruto',
    'polozajni_dodatek_pravosodje_c302bruto',
    'polozajni_dodatek_pravosodje_c303bruto',
    'polozajni_dodatek_pravosodje_c304bruto',
    'polozajni_dodatek_pravosodje_c305bruto',
    'polozajni_dodatek_pravosodje_c306bruto',
    'polozajni_dodatek_pravosodje_c307bruto',
    'polozajni_dodatek_pravosodje_c308bruto',
    'polozajni_dodatek_pravosodje_c309bruto',
    'polozajni_dodatek_pravosodje_c310bruto',
    'polozajni_dodatek_pravosodje_c311bruto',
    'polozajni_dodatek_pravosodje_c312bruto',
    'polozajni_dodatek_pravosodje_c313bruto',
    'dodatek_omejitev_pravice_do_stavke_c320bruto',
    'dodatek_za_dosegljivost_c321bruto',
    'dodatek_premestljive_sile_c322bruto',
    'dodatek_odzivne_sile_c323bruto',
    'dodatek_usposabljanje_c324bruto',
    'polozajni_dodatek_pravosodje_c330bruto',
    'polozajni_dodatek_pravosodje_c340bruto',
    'polozajni_dodatek_pravosodje_c350bruto',
    'polozajni_dodatek_pravosodje_c360bruto',
    'polozajni_dodatek_pravosodje_c370bruto',
    'polozajni_dodatek_pravosodje_c380bruto',
    'dodatek_mobilnost_c390bruto',
    'dodatek_izgradnja_kariere_c400bruto',
    'dodatek_poracun_c900bruto',
    # TODO not sure if these should be here
    'dodatki_delo_prek_polnega_casa_koriscenje_ur_e060bruto',
    'dodatki_delo_nedelja_koriscenje_ur_e061bruto',
    'dodatki_delo_nedelja_koriscenje_ur_e062bruto',
    'dodatki_delo_prost_dan_koriscenje_ur_e063bruto',
    'dodatki_delo_nedelja_nocno_koriscenje_ur_e064bruto',
    'dodatki_delo_prost_dan_nocno_koriscenje_ur_e065bruto'
    # precalculated and not included here
    # 'polozajni_dodatek',
    # 'ostali_dodatki',
]

BONUS_COLS = [
    'delovna_uspesnost_d010bruto',
    'delovna_uspesnost_sodniki_d011bruto',
    'delovna_uspesnost_tozilci_d012bruto',
    'delovna_uspesnost_pravobranilci_d013bruto',
    'delovna_uspesnost_povecan_obseg_dela_d020bruto',
    'delovna_uspesnost_ustavno_sodisce_d021bruto',
    'delovna_uspesnost_d022bruto',
    'delovna_uspesnost_d023bruto',
    'delovna_uspesnost_d024bruto',
    'delovna_uspesnost_povecan_obseg_dela_d025bruto',
    'delovna_uspesnost_posebni_projekti_d026bruto',
    'delovna_uspesnost_posebni_projekti_d027bruto',
    'delovna_uspesnost_prodaja_d030bruto',
    'delovna_uspesnost_59_clen_zsslov_040bruto',
    'delovna_uspesnost_povecan_obseg_dela_d041bruto',
    'delovna_uspesnost_59_clen_zsslov_d050bruto',
    'delovna_uspesnost_povecan_obseg_dela_d060bruto',
    'delovna_uspesnost_pedagoska_d070bruto',
    'delovna_uspesnost_pedagoska_d071bruto',
    'delovna_uspesnost_poracun_d900bruto',
    'delo_prek_polnega_casa_e010bruto',
    'delo_nocno_delo_e020bruto',
    'delo_nedelja_e030bruto',
    'delo_prost_dan_e031bruto',
    'delo_nedelja_nocno_e040bruto',
    'delo_prost_dan_nocno_e041bruto',
    'delo_prek_polnega_casa_e050bruto',
    'delo_prek_polnega_casa_pravosodje_e051bruto',
    # TODO not sure if these should be here
    'delo_prek_polnega_casa_poracun_e900bruto',
    'dezurstvo_preko_delovnega_casa_o010bruto',
    'dezurstvo_nocni_o020bruto',
    'dezurstvo_pravosodje_o030bruto',
    'dezurstvo_nedelja_o031bruto',
    'dezurstvo_dela_prost_dan_o032bruto',
    'dezurstvo_nocno_pravosodje_o040bruto',
    'dezurstvo_nedelja_nocno_o041bruto',
    'dezurstvo_dela_prost_dan_nocno_o042bruto',
    'dezurstvo_pravosodje_o050bruto',
    'dezurstvo_prek_polnega_casa_ju_o060bruto',
    'dezurstvo_nocno_ju_o070bruto',
    'dezurstvo_nedelja_ju_o080bruto',
    'dezurstvo_dela_prost_dan_ju_o090bruto',
    'dezurstvo_nedelja_nocno_ju_o100bruto',
    'dezurstvo_dela_prost_dan_nocno_ju_o110bruto',
    'dezurstvo_poracun_o900bruto'   # TODO ???
    # precalculated and not included here
    # 'delovna_uspesnost',
    # 'dodatno_delo',
    # 'dezurstvo'
]

def read_args():
    if len(sys.argv) < 3:
        print 'Run command: transform.py in_file out_file'
        exit(1)
    
    script = sys.argv[0]
    f_in = sys.argv[1]
    f_out = sys.argv[2]
    
    print 'Running \'' + script + '\''
    
    return f_in, f_out

def calc_addons(row, addon_cols):
    addon_pos = 0
    addon_neg = 0
    addon_pos_count = 0
    addon_neg_count = 0
    for addon in addon_cols:
        val = float(row[addon])
        if val > 0:
            addon_pos += val
            addon_pos_count += 1
        elif val < 0:
            addon_neg += val
            addon_neg_count += 1
            
    return addon_pos_count, addon_pos, addon_neg_count, addon_neg

def calc_accessories(row):
    '''Calculates the positive and negative accessories (dodatki) along with their counts'''
    return calc_addons(row, ACCESORY_COLS)

def calc_bonuses(row):
    '''Calculates the positive and negative bonuses (dodatki) along with their counts'''
    return calc_addons(row, BONUS_COLS)

def transform(f_in, f_out):
    print 'reading input file ...'
    
    data = list(csv.DictReader(open(f_in, 'rU')))
    writer = csv.DictWriter(f_out, fieldnames=OUT_FIELDS)
    
    print str(len(data))
    
    writer.writeheader()
    for i, row in data:
        if i % 1000 == 0:
            print str(i)
        
        try:
            employee_id = row['sifra_zaposlenega_z360']
            time = datetime.datetime(year=int(row['leto_obracuna']), month=int(row['mesec_obracuna']))
            salary = row['placa']
            diff_min_salary = row['placa_razlika_do_min_place_a020bruto']
            ministry_code = row['sifra_pu']
            ministry_name = row['naziv_pu']
            position = row['sifra_delovnega_mesta_z370']
            position_desc = row['opis_delovnega_mesta_z370opis']
            payment_grade = row['placni_razred_z380']  # placilni razred
            
            acc_pos_count, acc_pos, acc_neg_count, acc_neg = calc_accessories(row)
            bonus_pos_count, bonus_pos, bonus_neg_count, bonus_neg = calc_bonuses(row)
            
            # write to output
            writer.writerow({
                'id': employee_id,
                'cas': time,
                'ministry_id': ministry_code,
                'ministry_desc': ministry_name,
                'delovno_mesto': position,
                'delovno_mesto_desc': position_desc,
                'placilni_razred': payment_grade,
                'placa': salary,
                'razlika_minimalec': diff_min_salary,
                'stevilo_dodatkov_pos': acc_pos_count,
                'vsota_dodatkov_pos': acc_pos,
                'stevilo_dodatkov_neg': acc_neg_count,
                'vsota_dodatkov_neg': acc_neg,
                'stevilo_bonusov_pos': bonus_pos_count,
                'vsota_bonusov_pos': bonus_pos,
                'stevilo_bonusov_neg': bonus_neg_count,
                'vsota_bonusov_neg': bonus_neg
            })
            
        except Exception:
            print 'Could not parse row: ' + i
            traceback.format_exc()
        
    
# read CMD arguments to extract the file path
f_in, f_out = read_args()
# read the input file
transform(f_in, f_out)