from toee import *

def OnBeginSpellCast(spell):
    print "Curse of Impending Blades OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-necromancy-conjure",spell.caster) #does not do anything, commented out

def OnSpellEffect(spell):
    print "Curse of Impending Blades OnSpellEffect"
    
    spell.duration = 10 * spell.caster_level # 1 min/cl
    spellTarget = spell.target_list[0]

    #Spell has no Saving Throw
    spellTarget.obj.float_text_line("Curse of Impending Blades", tf_red)
    game.create_history_freeform(spellTarget.obj.description + " is affected by ~Curse of Impending Blades~[TAG_SPELLS_CURSE_OF_IMPENDING_BLADES]\n\n")
    spellTarget.obj.condition_add_with_args('sp-Curse of Impending Blades', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Phantasmal Killer', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Curse of Impending Blades OnBeginRound"

def OnEndSpellCast(spell):
    print "Curse of Impending Blades OnEndSpellCast"