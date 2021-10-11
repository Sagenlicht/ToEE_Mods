from toee import *
from utilities import *
from SummonMonsterTools import *

def OnBeginSpellCast( spell ):
    print "Summon Undead I OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect ( spell ):
    print "Summon Undead I OnSpellEffect"
    spell.duration = 1 * spell.caster_level
    undeadToSummon = spell.spell_get_menu_arg(RADIAL_MENU_PARAM_MIN_SETTING)
    possibleUndeadSummons =[14107, "Zombie 1HD"] #Skeleton 1HD; there are no more HD 1 undead in ToEE protos

    if undeadToSummon not in possibleUndeadSummons: #fallback
        undeadToSummon = 14107 #Skeleton 1HD

    spell.summon_monsters(1, undeadToSummon)
    summonedMonster = spell.target_list[0].obj
    game.particles('sp-Summon Monster I', summonedMonster)

    SummonMonster_Rectify_Initiative(spell, undeadToSummon) # Took this from Summon Monster; could also set intitiative manually

    spell.spell_end(spell.id)

def OnBeginRound( spell ):
    print "Summon Undead I OnBeginRound"

def OnEndSpellCast( spell ):
    print "Summon Undead I OnEndSpellCast"
