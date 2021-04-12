from toee import *

def OnBeginSpellCast(spell):
    print "Wave of Grief OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles( "sp-Transmutation-conjure", spell.caster )

def OnSpellEffect(spell):
    print "Wave of Grief OnSpellEffect"

    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/cl
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    game.particles('sp-Sound Burst', spell.caster)

    #get all targets in a 30 ft cone
    for spellTarget in spell.target_list:
        #Saving Throw to negate
        if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
            game.particles('Fizzle', spellTarget.obj)
            targetsToRemove.append(spellTarget.obj)
        else:
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.partsys_id = game.particles('sp-Shout-Hit', spellTarget.obj)
            spellTarget.obj.condition_add_with_args('sp-Wave of Grief', spell.id, spell.duration) # int(spellEnum)
    
    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Wave of Grief OnBeginRound"

def OnEndSpellCast(spell):
    print "Wave of Grief OnEndSpellCast"