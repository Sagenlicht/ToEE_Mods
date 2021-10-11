from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Fell the Greatest Foe"

def fellTheGreatestFoeSpellBonusToDamage(attachee, args, evt_obj):
    target =  evt_obj.attack_packet.target
    attackerSize = attachee.stat_level_get(stat_size)
    targetSize = target.stat_level_get(stat_size)
    bonusDiceNumber = targetSize-attackerSize

    #Fell the Greatest Foe only works with melee attacks
    if not evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        if bonusDiceNumber > 0:
            bonusDice = dice_new('1d6')
            bonusDice.number = bonusDiceNumber
            evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3003) #ID3003 added in damage.mes
    return 0

fellTheGreatestFoeSpell = PythonModifier("sp-Fell the Greatest Foe", 3, False) # spell_id, duration, empty
fellTheGreatestFoeSpell.AddHook(ET_OnDealingDamage, EK_NONE, fellTheGreatestFoeSpellBonusToDamage,())
fellTheGreatestFoeSpell.AddHook(ET_OnConditionAddPre, EK_NONE, spell_utils.replaceCondition, ())
fellTheGreatestFoeSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
fellTheGreatestFoeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
fellTheGreatestFoeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
fellTheGreatestFoeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
fellTheGreatestFoeSpell.AddSpellDispelCheckStandard()
fellTheGreatestFoeSpell.AddSpellTeleportPrepareStandard()
fellTheGreatestFoeSpell.AddSpellTeleportReconnectStandard()
fellTheGreatestFoeSpell.AddSpellCountdownStandardHook()
