from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Wave of Grief"

def waveOfGriefSpellPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-3,0,"~Wave of Grief~[TAG_SPELLS_WAVE_OF_GRIEF] Penalty") #Wave of Grief is a -3 penalty on Attack Rolls, saves and ability and skill checks
    return 0

def waveOfGriefSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Wave of Grief (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Wave of Grief (" + str(args.get_arg(1)) + " rounds)")
    return 0

def waveOfGriefSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WAVE_OF_GRIEF"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("WAVE_OF_GRIEF"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def waveOfGriefSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def waveOfGriefSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def waveOfGriefSpellSpellEnd(attachee, args, evt_obj):
    print "Wave of Grief SpellEnd"
    return 0

waveOfGriefSpell = PythonModifier("sp-Wave of Grief", 2) # spell_id, duration
waveOfGriefSpell.AddHook(ET_OnToHitBonus2, EK_NONE, waveOfGriefSpellPenalty,())
waveOfGriefSpell.AddHook(ET_OnGetSkillLevel, EK_NONE, waveOfGriefSpellPenalty,())
waveOfGriefSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, waveOfGriefSpellPenalty,())
waveOfGriefSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, waveOfGriefSpellPenalty,())
waveOfGriefSpell.AddHook(ET_OnGetTooltip, EK_NONE, waveOfGriefSpellTooltip, ())
waveOfGriefSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, waveOfGriefSpellEffectTooltip, ())
waveOfGriefSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, waveOfGriefSpellSpellEnd, ())
waveOfGriefSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, waveOfGriefSpellHasSpellActive, ())
waveOfGriefSpell.AddHook(ET_OnD20Signal, EK_S_Killed, waveOfGriefSpellKilled, ())
waveOfGriefSpell.AddSpellDispelCheckStandard()
waveOfGriefSpell.AddSpellTeleportPrepareStandard()
waveOfGriefSpell.AddSpellTeleportReconnectStandard()
waveOfGriefSpell.AddSpellCountdownStandardHook()
