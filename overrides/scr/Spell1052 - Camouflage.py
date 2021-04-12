from toee import *

def OnBeginSpellCast(spell):
    print "Camouflage OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-transmutation-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Camouflage OnSpellEffect"

    spell.duration = 100 * spell.caster_level # 10 min/cl
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Camouflage', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Meld into Stone', spellTarget.obj)
    
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Camouflage OnBeginRound"

def OnEndSpellCast(spell):
    print "Camouflage OnEndSpellCast"