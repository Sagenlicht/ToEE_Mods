from toee import *

def OnBeginSpellCast(spell):
    print "Nauseating Breath OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Nauseating Breath OnSpellEffect"

    targetsToRemove = []
    spellDurationDice = dice_new('1d6')

    game.particles('sp-Nauseating Breath', spell.caster)
    for spellTarget in spell.target_list:
        #Saving throw to negate nausea
        if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Fortitude, D20STD_F_NONE, spell.caster, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
        else:
            spell.duration = spellDurationDice.roll()
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.obj.condition_add_with_args('Nauseated Condition', spell.duration, 0, 0)
        targetsToRemove.append(spellTarget.obj)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Nauseating Breath OnBeginRound"

def OnEndSpellCast(spell):
    print "Nauseating Breath OnEndSpellCast"

