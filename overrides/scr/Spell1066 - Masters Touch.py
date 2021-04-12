from toee import *

def OnBeginSpellCast(spell):
    print "Masters Touch OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-divination-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Masters Touch OnSpellEffect"
    spell.duration = 10 * spell.caster_level # 1 Min/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])
    
    mastersTouchPossiblyTargetSlots = []
    mastersTouchPossiblyTargetSlots.append(spell.caster.item_worn_at(item_wear_weapon_primary)) #mainhand
    mastersTouchPossiblyTargetSlots.append(spell.caster.item_worn_at(item_wear_weapon_secondary)) #offhand
    mastersTouchPossiblyTargetSlots.append(spell.caster.item_worn_at(item_wear_shield)) #shield
    
    casterHasProficiency = False
    casterBaseProficiencies = []
    weaponProficiencyBard = [wt_sap, wt_short_sword, wt_longsword, wt_rapier, wt_shortbow, wt_composite_shortbow, wt_whip]
    weaponProficiencyDruid = [wt_dagger, wt_sickle, wt_club, wt_shortspear, wt_quarterstaff, wt_spear, wt_dart, wt_sling, wt_scimitar, wt_longspear]
    weaponProficiencyMonk = [wt_dagger, wt_club, wt_quarterstaff, wt_light_crossbow, wt_sling, wt_heavy_crossbow, wt_javelin, wt_handaxe, wt_kama, wt_nunchaku, wt_siangham, wt_shuriken]
    weaponProficiencyRogue = [wt_hand_crossbow, wt_rapier, wt_short_sword, wt_sap, wt_shortbow, wt_composite_shortbow]
    weaponProficiencyWizard = [wt_dagger, wt_club, wt_quarterstaff, wt_light_crossbow, wt_heavy_crossbow]
    weaponProficiencyElf = [wt_longsword, wt_rapier, wt_shortbow, wt_composite_shortbow, wt_longbow, wt_composite_longbow]
    if spell.caster.has_feat(feat_simple_weapon_proficiency_bard):
        casterBaseProficiencies.extend(weaponProficiencyBard)
        hasFullSimpleProficiency = True
    if spell.caster.has_feat(feat_simple_weapon_proficiency_druid):
        casterBaseProficiencies.extend(weaponProficiencyDruid)
    if spell.caster.has_feat(feat_simple_weapon_proficiency_monk):
        casterBaseProficiencies.extend(weaponProficiencyMonk)
    if spell.caster.has_feat(feat_simple_weapon_proficiency_rogue):
        casterBaseProficiencies.extend(weaponProficiencyRogue)
        hasFullSimpleProficiency = True
    if spell.caster.has_feat(feat_simple_weapon_proficiency_wizard):
        casterBaseProficiencies.extend(weaponProficiencyWizard)
    if spell.caster.has_feat(feat_simple_weapon_proficiency_elf):
        casterBaseProficiencies.extend(weaponProficiencyElf)
    
    if spellTarget.obj == OBJ_HANDLE_NULL:
        spell.caster.float_text_line("No item equipped", tf_red)
        game.particles( 'Fizzle', spell.caster )
        spell.target_list.remove_target( spellTarget.obj)
    else:
        try: #Masters Gift only works on equipped items in main or offhand
            itemSlot = mastersTouchPossiblyTargetSlots.index(spellTarget.obj)
        except ValueError:
            spell.caster.float_text_line("Item must be an equipped weapon or shield")
            game.particles('Fizzle', spell.caster)
            spell.target_list.remove_target(spellTarget.obj)
        else:
            if itemSlot == 0:
                wornItemType = spell.caster.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_weapon_type) #Get weapon type mainhand
            elif itemSlot == 1:
                wornItemType = spell.caster.item_worn_at(item_wear_weapon_secondary).obj_get_int(obj_f_weapon_type) #Get weapon type offhand
            else:
                wornItemType = 0
            #check for Proficiency
            if wornItemType == 0:
                if spell.caster.has_feat(feat_shield_proficiency): #check if caster is already proficient with shields; Tower Shields don't seem to differenciate???
                    casterHasProficiency = True
            else:
                featNeeded = game.get_feat_for_weapon_type(wornItemType)
                if spell.caster.has_feat(featNeeded):
                    casterHasProficiency = True
                if spell.caster.has_feat(feat_martial_weapon_proficiency_all):
                    if featNeeded in range(228, 259): #range inlcudes lower and excludes upper value
                        casterHasProficiency = True
                if featNeeded == 281: #every simple weapon returns 281 when quering game.get_feat_for_weapon_type(wornItemType)
                    if hasFullSimpleProficiency:
                        casterHasProficiency = True
                if wornItemType in casterBaseProficiencies:
                    casterHasProficiency = True
            
            if not casterHasProficiency:
                spell.caster.condition_add_with_args('sp-Masters Touch', spell.id, spell.duration, wornItemType) #int(spellEnum)
                spellTarget.partsys_id = game.particles('sp-Detect Magic 2 Med', spell.caster)
            else:
                spell.caster.float_text_line("Already proficient")
                game.particles('Fizzle', spell.caster)
                spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end( spell.id)

def OnBeginRound(spell):
    print "Masters Touch OnBeginRound"

def OnEndSpellCast(spell):
    print "Masters Touch OnEndSpellCast"