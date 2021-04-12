from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Sticky Fingers"

def stickyFingersSpellBonusToSoH(attachee, args, evt_obj):
    evt_obj.bonus_list.add(10, 0, "~Sticky Fingers~[TAG_SPELLS_STICKY_FINGERS] Bonus") # Sticky Fingers is a flat +10 untyped bouns to Sleight of Hand checks
    return 0

def stickyFingersSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Sticky Fingers (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Sticky Fingers (" + str(args.get_arg(1)) + " rounds)")
    return 0

def stickyFingersSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("STICKY_FINGERS"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("STICKY_FINGERS"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def stickyFingersSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def stickyFingersSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def stickyFingersSpellSpellEnd(attachee, args, evt_obj):
    print "Sticky Fingers SpellEnd"
    return 0

stickyFingersSpell = PythonModifier("sp-Sticky Fingers", 2) # spell_id, duration
stickyFingersSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_PICK_POCKET, stickyFingersSpellBonusToSoH,())
stickyFingersSpell.AddHook(ET_OnGetTooltip, EK_NONE, stickyFingersSpellTooltip, ())
stickyFingersSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, stickyFingersSpellEffectTooltip, ())
stickyFingersSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, stickyFingersSpellSpellEnd, ())
stickyFingersSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, stickyFingersSpellHasSpellActive, ())
stickyFingersSpell.AddHook(ET_OnD20Signal, EK_S_Killed, stickyFingersSpellKilled, ())
stickyFingersSpell.AddSpellDispelCheckStandard()
stickyFingersSpell.AddSpellTeleportPrepareStandard()
stickyFingersSpell.AddSpellTeleportReconnectStandard()
stickyFingersSpell.AddSpellCountdownStandardHook()
