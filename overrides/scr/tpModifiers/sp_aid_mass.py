from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Aid Mass"

def aidMassSpellBonusToHit(attachee, args, evt_obj):
    evt_obj.bonus_list.add(1, 13,"~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]") #ID 13 = Morale
    return 0

def aidMassSpellSaveBonus(attachee, args, evt_obj):
    if evt_obj.flags & 0x100000: #d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_FEAR = 21, // 0x100000
        evt_obj.bonus_list.add(1, 13,"~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]") #ID 13 = Morale
    return 0

def aidMassSpellRemoveTempHp(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, 'Temporary_Hit_Points')
    return 0

def aidMassSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Aid Mass ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Aid Mass ({} rounds)".format(args.get_arg(1)))
    return 0

def aidMassSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("AID_MASS"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("AID_MASS"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def aidMassSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def aidMassSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def aidMassSpellSpellEnd(attachee, args, evt_obj):
    print "Aid Mass SpellEnd"
    return 0

aidMassSpell = PythonModifier("sp-Aid Mass", 2) # spell_id, duration
aidMassSpell.AddHook(ET_OnToHitBonus2, EK_NONE, aidMassSpellBonusToHit, ())
aidMassSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, aidMassSpellSaveBonus, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, aidMassSpellRemoveTempHp, ())
aidMassSpell.AddHook(ET_OnGetTooltip, EK_NONE, aidMassSpellTooltip, ())
aidMassSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, aidMassSpellEffectTooltip, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, aidMassSpellSpellEnd, ())
aidMassSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, aidMassSpellHasSpellActive, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Killed, aidMassSpellKilled, ())
aidMassSpell.AddSpellDispelCheckStandard()
aidMassSpell.AddSpellTeleportPrepareStandard()
aidMassSpell.AddSpellTeleportReconnectStandard()
aidMassSpell.AddSpellCountdownStandardHook()
