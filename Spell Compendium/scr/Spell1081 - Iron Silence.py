from toee import *

def OnBeginSpellCast(spell):
    print "Iron Silence OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-divination-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Iron Silence OnSpellEffect"
    spell.duration = 100 * spell.caster_level # 1 Min/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    casterHasProficiency = False
    wornArmor = spell.caster.item_worn_at(item_wear_armor)
    
    if wornArmor == OBJ_HANDLE_NULL:
        spell.caster.float_text_line("No Armor equipped", tf_red)
        game.particles( 'Fizzle', spell.caster )
        spell.target_list.remove_target( spellTarget.obj)

    else:
        wornArmorType = wornArmor.obj_get_int(obj_f_armor_flags)

        #check for Proficiency
        if wornArmorType == 0:
            if spell.caster.has_feat(feat_armor_proficiency_light):
                casterHasProficiency = True
        elif wornArmorType == 1:
            if spell.caster.has_feat(feat_armor_proficiency_medium):
                casterHasProficiency = True
        elif wornArmorType == 2:
            if spell.caster.has_feat(feat_armor_proficiency_heavy):
                casterHasProficiency = True
        else:
            print wornArmorType
            casterHasProficiency = True

        if casterHasProficiency:
                spell.caster.condition_add_with_args('sp-Iron Silence', spell.id, spell.duration)  #int(spellEnum)
                spellTarget.partsys_id = game.particles('sp-Detect Magic 2 Med', spell.caster)
        else:
            spell.caster.float_text_line("Not proficient with armor")
            game.particles('Fizzle', spell.caster)
            spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end( spell.id)

def OnBeginRound(spell):
    print "Iron Silence OnBeginRound"

def OnEndSpellCast(spell):
    print "Iron Silence OnEndSpellCast"