from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Fell the Greatest Foe"

def fellTheGreatestFoeSpellBonusToDamage(attachee, args, evt_obj):
    targetToHit =  evt_obj.attack_packet.target
    attackerSize = attachee.stat_level_get(stat_size)
    targetSize = targetToHit.stat_level_get(stat_size)
    bonusDiceNumber = targetSize-attackerSize
    
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED: #Fell the Greatest Foe only works with melee attacks
        return 0

    if bonusDiceNumber > 0:
        bonusDice = dice_new('1d6')
        bonusDice.number = bonusDiceNumber
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3003) #ID3003 added in damage.mes
    return 0
    
def fellTheGreatestFoeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Fell the Greatest Foe ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Fell the Greatest Foe ({} rounds)".format(args.get_arg(1)))
    return 0

def fellTheGreatestFoeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FELL_THE_GREATEST_FOE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FELL_THE_GREATEST_FOE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def fellTheGreatestFoeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def fellTheGreatestFoeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def fellTheGreatestFoeSpellSpellEnd(attachee, args, evt_obj):
    print "Fell the Greatest Foe SpellEnd"
    return 0

fellTheGreatestFoeSpell = PythonModifier("sp-Fell the Greatest Foe", 2) # spell_id, duration
fellTheGreatestFoeSpell.AddHook(ET_OnDealingDamage, EK_NONE, fellTheGreatestFoeSpellBonusToDamage,())
fellTheGreatestFoeSpell.AddHook(ET_OnGetTooltip, EK_NONE, fellTheGreatestFoeSpellTooltip, ())
fellTheGreatestFoeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, fellTheGreatestFoeSpellEffectTooltip, ())
fellTheGreatestFoeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, fellTheGreatestFoeSpellSpellEnd, ())
fellTheGreatestFoeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, fellTheGreatestFoeSpellHasSpellActive, ())
fellTheGreatestFoeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, fellTheGreatestFoeSpellKilled, ())
fellTheGreatestFoeSpell.AddSpellDispelCheckStandard()
fellTheGreatestFoeSpell.AddSpellTeleportPrepareStandard()
fellTheGreatestFoeSpell.AddSpellTeleportReconnectStandard()
fellTheGreatestFoeSpell.AddSpellCountdownStandardHook()
