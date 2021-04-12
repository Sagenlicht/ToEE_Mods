from toee import *

def OnBeginSpellCast(spell):
    print "Undersong OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-Transmutation-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Undersong OnSpellEffect"

    spell.duration = 100 * spell.caster_level # 10 min/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    spellTarget.obj.condition_add_with_args('sp-Undersong', spell.id, spell.duration) #int(spellEnum)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Undersong OnBeginRound"

def OnEndSpellCast(spell):
    print "Undersong OnEndSpellCast"