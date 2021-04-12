from toee import *

def OnBeginSpellCast(spell):
    print "Shock and Awe OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-Enchantment-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Shock and Awe OnSpellEffect"

    targetsToRemove = []
    spell.duration = 0 # 1 round
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    game.particles('sp-Shock and Awe', spell.caster)

    #check if Surprise Round
    #don't know yet how to check this

    #The spell does not have a saving throw!
    for spellTarget in spell.target_list:
        if spellTarget.obj.d20_query(Q_Flatfooted) == 1: #Only flatfooted targets are valid targets
            spellTarget.obj.d20_status_init()
            spellTargetInitiative = spellTarget.obj.get_initiative()
            spellTarget.obj.set_initiative((spellTargetInitiative-10))
            spellTarget.partsys_id = game.particles('sp-Shout-Hit', spellTarget.obj)
        else:
            spellTarget.obj.float_text_line("Not flatfooted")
            game.particles('Fizzle', spellTarget.obj)
        targetsToRemove.append(spellTarget.obj) #no condition added, so every target is removed

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Shock and Awe OnBeginRound"

def OnEndSpellCast(spell):
    print "Shock and Awe OnEndSpellCast"