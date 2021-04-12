from toee import *

def OnBeginSpellCast(spell):
    print "Harmonic Chorus OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles( "sp-divination-conjure", spell.caster )

def OnSpellEffect(spell):
    print "Harmonic Chorus OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    spellTarget.obj.condition_add_with_args('sp-Harmonic Chorus', spell.id, spell.duration) # int(spellEnum)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Harmonic Chorus OnBeginRound"

def OnEndSpellCast(spell):
    print "Harmonic Chorus OnEndSpellCast"