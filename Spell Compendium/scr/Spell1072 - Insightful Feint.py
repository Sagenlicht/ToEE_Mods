from toee import *

def OnBeginSpellCast(spell):
    print "Insightful Feint OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-divination-conjure",spell.caster )

def OnSpellEffect(spell):
    print "Insightful Feint OnSpellEffect"
    
    spell.duration = 0 #Feint action needs to be done in same round
    spellTarget = spell.target_list[0]
    
    spellTarget.obj.condition_add_with_args('sp-Insightful Feint', spell.id, spell.duration)
    #spellTarget.partsys_id = game.particles('sp-Meld into Stone', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Insightful Feint OnBeginRound"

def OnEndSpellCast(spell):
    print "Insightful Feint OnEndSpellCast"