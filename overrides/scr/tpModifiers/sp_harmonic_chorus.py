from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Harmonic Chorus"

def harmonicChorusSpellBonusToDc(attachee, args, evt_obj):
    evt_obj.bonus_list.add(2,13,"~Harmonic Chorus~[TAG_SPELLS_HARMONIC_CHORUS] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Harmonic Chorus is a +2 morale bouns to caster level and spell dc
    return 0

def harmonicChorusSpellBonusToCasterLevel(attachee, args, evt_obj):
    evt_obj.return_val += 2
    return 0

def harmonicChorusSpellAddConcentration(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.caster.condition_add_with_args('sp-Concentrating', args.get_arg(0))
    #spellPacket.caster.condition_add_with_args('Dismiss', args.get_arg(0))
    return 0

def harmonicChorusSpellConcentrationBroken(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.spell_enum == 0:
        return 0
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def harmonicChorusSpellDismissed(attachee, args, evt_obj):
    if evt_obj.data1 == args.get_arg(0):
        args.remove_spell()
        args.remove_spell_mod()
    return 0

def harmonicChorusSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Harmonic Chorus ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Harmonic Chorus ({} rounds)".format(args.get_arg(1)))
    return 0

def harmonicChorusSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("HARMONIC_CHORUS"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("HARMONIC_CHORUS"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def harmonicChorusSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def harmonicChorusSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def harmonicChorusSpellSpellEnd(attachee, args, evt_obj):
    print "harmonicChorusSpellSpellEnd"
    return 0

harmonicChorusSpell = PythonModifier("sp-Harmonic Chorus", 2) # spell_id, duration
harmonicChorusSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, harmonicChorusSpellBonusToCasterLevel,())
harmonicChorusSpell.AddHook(ET_OnGetSpellDcMod , EK_NONE, harmonicChorusSpellBonusToDc,())
harmonicChorusSpell.AddHook(ET_OnConditionAdd, EK_NONE, harmonicChorusSpellAddConcentration,())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, harmonicChorusSpellConcentrationBroken, ())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, harmonicChorusSpellDismissed, ())
harmonicChorusSpell.AddHook(ET_OnGetTooltip, EK_NONE, harmonicChorusSpellTooltip, ())
harmonicChorusSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, harmonicChorusSpellEffectTooltip, ())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, harmonicChorusSpellSpellEnd, ())
harmonicChorusSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, harmonicChorusSpellHasSpellActive, ())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Killed, harmonicChorusSpellKilled, ())
harmonicChorusSpell.AddSpellDispelCheckStandard()
harmonicChorusSpell.AddSpellTeleportPrepareStandard()
harmonicChorusSpell.AddSpellTeleportReconnectStandard()
harmonicChorusSpell.AddSpellCountdownStandardHook()
harmonicChorusSpell.AddSpellDismissStandardHook()
