from toee import *

def OnBeginSpellCast(spell):
    print "Snipers Shot OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-divination-conjure",spell.caster )

def OnSpellEffect(spell):
    print "Snipers Shot OnSpellEffect"
    
    spell.duration = 0 #Snipers Shot is a Swift Action, works in the current round
    spellTarget = spell.target_list[0]
    
    spellTarget.obj.condition_add_with_args('sp-Snipers Shot', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-True Strike', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Snipers Shot OnBeginRound"

def OnEndSpellCast(spell):
    print "Snipers Shot OnEndSpellCast"