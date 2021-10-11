from toee import *

def OnBeginSpellCast(spell):
    print "Nimbus of Light OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Nimbus of Light OnSpellEffect"

    spell.duration = 10 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Nimbus of Light', spell.id, spell.duration, 0, 0) #3rd arg = roundsCharged; 4th arg = attack_hit_status
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Nimbus of Light OnBeginRound"

def OnEndSpellCast(spell):
    print "Nimbus of Light OnEndSpellCast"

