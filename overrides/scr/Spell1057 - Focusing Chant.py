from toee import *

def OnBeginSpellCast(spell):
    print "Focusing Chant OnBeginSpellCast"
    print "spell.spellTarget_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-Enchantment-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Focusing Chant OnSpellEffect"

    spell.duration = 10 # 1 Minute
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    spellTarget.obj.condition_add_with_args('sp-Focusing Chant', spell.id, spell.duration) #int(spellEnum)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Focusing Chant OnBeginRound"

def OnEndSpellCast(spell):
    print "Focusing Chant OnEndSpellCast"