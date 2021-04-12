from toee import *

def OnBeginSpellCast(spell):
    print "Bonefiddle OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-necromancy-conjure",spell.caster) #does not do anything, commented out

def OnSpellEffect(spell):
    print "Bonefiddle OnSpellEffect"
    
    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])
    
    spellTargetRacialImmunity = False
    immunityList = [mc_type_construct, mc_type_elemental, mc_type_plant, mc_type_ooze] #only targets creature with a skeleton or exoskeleton

    for spellTargetType in immunityList:
        if spellTarget.obj.is_category_type(spellTargetType):
            spellTargetRacialImmunity = True

    if spellTargetRacialImmunity or spellTarget.obj.is_category_subtype(mc_subtype_incorporeal): #incorporal are also invalid targets
        spellTarget.obj.float_text_line("Unaffected due to Racial Immunity") #Mimics the original game message
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)
    else:
        spellTarget.obj.condition_add_with_args('sp-Bonefiddle', spell.id, spell.duration, spell.dc) #int(spellEnum)
        spellTarget.partsys_id = game.particles('sp-Phantasmal Killer', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Bonefiddle OnBeginRound"

def OnEndSpellCast(spell):
    print "Bonefiddle OnEndSpellCast"