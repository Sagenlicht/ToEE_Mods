from toee import *

def OnBeginSpellCast(spell):
    print "Serene Visage OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-illusion-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Serene Visage OnSpellEffect"

    spell.duration = 10 * spell.caster_level # 1 Minute/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    bonusToBluff = min(max(1, (spell.caster_level/2)), 10) #Bonus is capped at 10; D&D rounds down, but I think to a minimum of 1. Maybe max(1 is not needed

    spellTarget.obj.condition_add_with_args('sp-Serene Visage', spell.id, spell.duration, bonusToBluff) #int(spellEnum)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Serene Visage OnBeginRound"

def OnEndSpellCast(spell):
    print "Serene Visage OnEndSpellCast"