from toee import *

def OnBeginSpellCast(spell):
    print "Strategic Charge OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Strategic Charge OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]

    if spellTarget.obj.has_feat(feat_mobility):
        spellTarget.float_text_line("Already has Mobility", tf_red)
        game.particles('Fizzle', spell.caster)
        spell.target_list.remove_target(spellTarget.obj)
    else:
        spellTarget.obj.condition_add_with_args('sp-Strategic Charge', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-Expeditious Retreat', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Strategic Charge OnBeginRound"

def OnEndSpellCast(spell):
    print "Strategic Charge OnEndSpellCast"