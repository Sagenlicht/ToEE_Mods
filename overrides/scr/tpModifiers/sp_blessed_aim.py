from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Blessed Aim"

def blessedAimSpellBonus(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(2, 21, "~Blessed Aim~[TAG_SPELLS_BLESSED_AIM] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Blessed Aim adds a +2 Morale Bonus to Ranged Attack Rolls
    return 0

def blessedAimSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Blessed Aim ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Blessed Aim ({} rounds)".format(args.get_arg(1)))
    return 0

def blessedAimSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BLESSED_AIM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BLESSED_AIM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def blessedAimSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def blessedAimSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def blessedAimSpellSpellEnd(attachee, args, evt_obj):
    print "Blessed Aim SpellEnd"
    return 0

blessedAimSpell = PythonModifier("sp-Blessed Aim", 2) # spell_id, duration
blessedAimSpell.AddHook(ET_OnToHitBonus2, EK_NONE, blessedAimSpellBonus,())
blessedAimSpell.AddHook(ET_OnGetTooltip, EK_NONE, blessedAimSpellTooltip, ())
blessedAimSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, blessedAimSpellEffectTooltip, ())
blessedAimSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, blessedAimSpellSpellEnd, ())
blessedAimSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, blessedAimSpellHasSpellActive, ())
blessedAimSpell.AddHook(ET_OnD20Signal, EK_S_Killed, blessedAimSpellKilled, ())
blessedAimSpell.AddSpellDispelCheckStandard()
blessedAimSpell.AddSpellTeleportPrepareStandard()
blessedAimSpell.AddSpellTeleportReconnectStandard()
blessedAimSpell.AddSpellCountdownStandardHook()
