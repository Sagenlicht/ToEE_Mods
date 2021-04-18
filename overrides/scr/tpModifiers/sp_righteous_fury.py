from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Righteous Fury"

def righteousFurySpellAbilityBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(4, 153, "~Sacred~[TAG_MODIFIER_SACRED] : ~Righteous Fury~[TAG_SPELLS_RIGHTEOUS_FURY] Bonus") #Righteous Fury adds a +4 Sacred Bonus to Strength
    return 0

def righteousFurySpellOnConditionAdd(attachee, args, evt_obj):
    attachee.condition_add_with_args('Temporary_Hit_Points', 0, 600, args.get_arg(2)) #temp HP value is passed by spell (arg3), duration is up to 1 hour;
    return 0

def righteousFurySpellRemoveTempHp(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, 'Temporary_Hit_Points')
    return 0

def righteousFurySpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Righteous Fury ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Righteous Fury ({} rounds)".format(args.get_arg(1)))
    return 0

def righteousFurySpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("RIGHTEOUS_FURY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("RIGHTEOUS_FURY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def righteousFurySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def righteousFurySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def righteousFurySpellSpellEnd(attachee, args, evt_obj):
    print "Righteous Fury SpellEnd"
    return 0

righteousFurySpell = PythonModifier("sp-Righteous Fury", 3) # spell_id, duration, tempHitPoints
righteousFurySpell.AddHook(ET_OnConditionAdd, EK_NONE, righteousFurySpellOnConditionAdd,())
righteousFurySpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_STRENGTH, righteousFurySpellAbilityBonus,())
righteousFurySpell.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, righteousFurySpellRemoveTempHp, ())
righteousFurySpell.AddHook(ET_OnGetTooltip, EK_NONE, righteousFurySpellTooltip, ())
righteousFurySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, righteousFurySpellEffectTooltip, ())
righteousFurySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, righteousFurySpellSpellEnd, ())
righteousFurySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, righteousFurySpellHasSpellActive, ())
righteousFurySpell.AddHook(ET_OnD20Signal, EK_S_Killed, righteousFurySpellKilled, ())
righteousFurySpell.AddSpellDispelCheckStandard()
righteousFurySpell.AddSpellTeleportPrepareStandard()
righteousFurySpell.AddSpellTeleportReconnectStandard()
righteousFurySpell.AddSpellCountdownStandardHook()
