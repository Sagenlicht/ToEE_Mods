from toee import *

def OnBeginSpellCast(spell):
    print "Aid Mass OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Aid Mass OnSpellEffect"

    spell.duration = 10 * spell.caster_level
    tempHp = dice_new('1d8')
    tempHp.bonus = min(spell.caster_level, 15)
    tempHpAmount = tempHp.roll()

    for spellTarget in spell.target_list:
        spellTarget.obj.condition_add_with_args('sp-Aid Mass', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-Aid', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Aid Mass OnBeginRound"

def OnEndSpellCast(spell):
    print "Aid Mass OnEndSpellCast"

