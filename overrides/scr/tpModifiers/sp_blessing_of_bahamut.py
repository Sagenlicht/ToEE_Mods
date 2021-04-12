from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Blessing of Bahamut"

def blessingOfBahamutSpellGrantDr(attachee, args, evt_obj):
    evt_obj.damage_packet.add_physical_damage_res(10, D20DAP_MAGIC, 126) #Blessing of Bahamut grants DR10/magic; ID126 in damage.mes is DR
    return 0

def blessingOfBahamutSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Blessing of Bahamut ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Blessing of Bahamut ({} rounds)".format(args.get_arg(1)))
    return 0

def blessingOfBahamutSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BLESSING_OF_BAHAMUT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BLESSING_OF_BAHAMUT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def blessingOfBahamutSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def blessingOfBahamutSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def blessingOfBahamutSpellSpellEnd(attachee, args, evt_obj):
    print "Blessing of Bahamut SpellEnd"
    return 0

blessingOfBahamutSpell = PythonModifier("sp-Blessing of Bahamut", 2) # spell_id, duration
blessingOfBahamutSpell.AddHook(ET_OnTakingDamage, EK_NONE, blessingOfBahamutSpellGrantDr,())
blessingOfBahamutSpell.AddHook(ET_OnGetTooltip, EK_NONE, blessingOfBahamutSpellTooltip, ())
blessingOfBahamutSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, blessingOfBahamutSpellEffectTooltip, ())
blessingOfBahamutSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, blessingOfBahamutSpellSpellEnd, ())
blessingOfBahamutSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, blessingOfBahamutSpellHasSpellActive, ())
blessingOfBahamutSpell.AddHook(ET_OnD20Signal, EK_S_Killed, blessingOfBahamutSpellKilled, ())
blessingOfBahamutSpell.AddSpellDispelCheckStandard()
blessingOfBahamutSpell.AddSpellTeleportPrepareStandard()
blessingOfBahamutSpell.AddSpellTeleportReconnectStandard()
blessingOfBahamutSpell.AddSpellCountdownStandardHook()
