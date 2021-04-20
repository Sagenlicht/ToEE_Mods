from toee import *

def OnBeginSpellCast(spell):
    print "Devil Blight OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Devil Blight OnSpellEffect"

    spellDurationDice = dice_new('1d6')
    spell.duration = spellDurationDice.roll()
    spellTarget = spell.target_list[0]
    spellTargetHasLawfulSubtype = spellTarget.obj.is_category_subtype(mc_subtype_lawful)
    spellTargetHasEvilSubtype = spellTarget.obj.is_category_subtype(mc_subtype_evil)
    spellTargetIsDevil = spellTarget.obj.is_category_subtype(mc_subtype_devil)

    if spellTargetHasLawfulSubtype and spellTargetHasEvilSubtype:
        hasNeededSubtypes = True
    else:
        hasNeededSubtypes = False
    if spellTarget.obj.is_category_type(mc_type_construct):
        isLiving = False
    elif spellTarget.obj.is_category_type(mc_type_undead):
        isLiving = False
    else:
        isLiving = True
    
    if isLiving and hasNeededSubtypes:
        spellTarget.obj.condition_add_with_args('sp-Demon Dirge', spell.id, spell.duration)
        game.particles('hit-HOLY-medium', spellTarget.obj)
        if spellTargetIsDevil:
            #Saving Throw to avoid stun
            game.create_history_freeform("{} saves versus ~Devil Blight~[TAG_SPELLS_DEVIL_BLIGHT] stun effect\n\n".format(spellTarget.obj.description))
            if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Fortitude, D20STD_F_NONE, spell.caster, spell.id): #success
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
            else:
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
                spellTarget.obj.condition_add_with_args('Stunned', (spell.duration +1), 0)
    else:
        if not isLiving:
            spellTarget.obj.float_text_line("Unaffected due to Racial Immunity")
        else:
            spellTarget.obj.float_text_line("Wrong Alignment")
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Devil Blight OnBeginRound"

def OnEndSpellCast(spell):
    print "Devil Blight OnEndSpellCast"

