from toee import *

def OnBeginSpellCast(spell):
    print "Sonic Weapon OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-divination-conjure",spell.caster )

def OnSpellEffect(spell):
    print "Sonic Weapon OnSpellEffect"
    
    spell.duration = 10 * spell.caster_level # 1 min/cl
    spellTarget = spell.target_list[0]
    #spellEnum = (str(spell)[str(spell).index('(')+len('('):str(spell).index(')')])

    spellTarget.obj.condition_add_with_args('sp-Sonic Weapon', spell.id, spell.duration) #int(spellEnum)
    spellTarget.partsys_id = game.particles('sp-Sound Burst', spellTarget.obj)

    spell.spell_end(spell.id)


def OnBeginRound(spell):
    print "Sonic Weapon OnBeginRound"

def OnEndSpellCast(spell):
    print "Sonic Weapon OnEndSpellCast"