from toee import *

def OnBeginSpellCast(spell):
    print "Weapon of the Deity OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Weapon of the Deity OnSpellEffect"

    spell.duration = 600 * spell.caster_level
    spellTarget = spell.target_list[0]
    spellCasterDeity = spell.caster.get_deity()
    weaponToHitBonus = min((1 + ((spell.caster_level - 6)/3)), 5) #capped at caster_level 18 at +5
    favoredWeapon = {
    DEITY_NONE: OBJ_HANDLE_NULL, #None
    DEITY_BOCCOB: wt_quarterstaff, #Boccob
    DEITY_CORELLON_LARETHIAN: wt_longsword, #Corellon Larethian
    DEITY_EHLONNA: wt_longsword, #Ehlonna
    DEITY_ERYTHNUL: wt_morningstar, #Erythnul
    DEITY_FHARLANGHN: wt_quarterstaff, #Fharlanghn
    DEITY_GARL_GLITTERGOLD: wt_battleaxe, #Garl Glittergold
    DEITY_GRUUMSH: wt_shortspear, #Gruumsh
    DEITY_HEIRONEOUS: wt_longsword, #Heironeous
    DEITY_HEXTOR: wt_heavy_flail, #Hextor
    DEITY_KORD: wt_greatsword, #Kord
    DEITY_MORADIN: [wt_warhammer, 'Weapon Frost'], #Moradin
    DEITY_NERULL: wt_scythe, #Nerull
    DEITY_OBAD_HAI: wt_quarterstaff, #Obad-Hai
    DEITY_OLIDAMMARA: wt_rapier, #Olidammara
    DEITY_PELOR: wt_heavy_mace, #Pelor
    DEITY_ST_CUTHBERT: wt_heavy_mace, #St. Cuthbert
    DEITY_VECNA: wt_dagger, #Vecna
    DEITY_WEE_JAS: wt_dagger, #Wee Jas
    DEITY_YONDALLA: wt_short_sword, #Yondalla
    DEITY_OLD_FAITH: 0, #wt_Old Faith
    DEITY_ZUGGTMOY: 0, #Zuggtmoy
    DEITY_IUZ: 0, #Iuz
    DEITY_LOLTH: wt_whip, #Lolth
    DEITY_PROCAN: 0, #Procan
    DEITY_NOREBO: 0, #Norebo
    DEITY_PYREMIUS: 0, #Pyremius
    DEITY_RALISHAZ: 0 #Ralishaz
    }
    wornWeapon = spellTarget.obj.item_worn_at(item_wear_weapon_primary)
    
    print "favoredWeapon Deity: ", favoredWeapon.get(spellCasterDeity)[0]
    if favoredWeapon.get(spellCasterDeity)[0] == spellTarget.obj.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_weapon_type):
        spellTarget.obj.condition_add_with_args('sp-Weapon of the Deity', spell.id, spell.duration, weaponToHitBonus, spellCasterDeity)
        wornWeapon.d20_status_init()
        print "Has already condition: ", wornWeapon.d20_query_has_condition('Weapon Defending Bonus')
        print "d20_query ", wornWeapon.d20_query('Weapon Defending Bonus')
        #print "d20_query_with_data ", wornWeapon.d20_query_with_data('Weapon Flaming')
        #print "d20_query_with_object ", wornWeapon.d20_query_with_object('Weapon Flaming')
        wornWeapon.item_condition_add_with_args(favoredWeapon.get(spellCasterDeity)[1], spell.duration, 0, 0)
        print "conditions_get(): ", spellTarget.obj.conditions_get()
        print "conditions_get() wornWeapon: ", wornWeapon.conditions_get()
        #spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)
    else:
        spell.caster.float_text_line("Favored weapon of deity required", tf_red)
        game.particles('Fizzle', spell.caster)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Weapon of the Deity OnBeginRound"

def OnEndSpellCast(spell):
    print "Weapon of the Deity OnEndSpellCast"

