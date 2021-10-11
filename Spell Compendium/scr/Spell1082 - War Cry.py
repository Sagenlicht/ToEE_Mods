from toee import *

def OnBeginSpellCast(spell):
    print "War Cry OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles( "sp-enchantme-conjure", spell.caster )

def OnSpellEffect(spell):
    print "War Cry OnSpellEffect"

    spell.duration = 0 # current round
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    game.particles('sp-Sound Burst', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-War Cry', spell.id, spell.duration, spell.dc, 0) # int(spellEnum)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "War Cry OnBeginRound"

def OnEndSpellCast(spell):
    print "War Cry OnEndSpellCast"