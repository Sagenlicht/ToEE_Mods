from toee import *

def OnBeginSpellCast(spell):
    print "Allegro OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Allegro OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 10 * spell.caster_level # 1 min/cl

    #game.particles('sp-Sound Burst', spell.caster)

    for spellTarget in spell.target_list:
        spellTarget.partsys_id = game.particles('sp-Expeditious Retreat', spellTarget.obj)
        spellTarget.obj.condition_add_with_args('sp-Allegro', spell.id, spell.duration, spell.dc)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Allegro OnBeginRound"

def OnEndSpellCast(spell):
    print "Allegro OnEndSpellCast"