from toee import *

def OnBeginSpellCast(spell):
    print "Bladeweave OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles( "sp-enchantme-conjure", spell.caster )

def OnSpellEffect(spell):
    print "Bladeweave OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    spellTarget.partsys_id = game.particles('sp-True Strike', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-Bladeweave', spell.id, spell.duration, spell.dc, 0) #int(spellEnum)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Bladeweave OnBeginRound"

def OnEndSpellCast(spell):
    print "Bladeweave OnEndSpellCast"