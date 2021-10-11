from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Righteous Fury"

def righteousFurySpellAbilityBonus(attachee, args, evt_obj):
    bonusValue = 4 #Righteous Fury adds a +4 Sacred Bonus to Strength
    bonusType = 153 #ID 153 = Sacred
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Sacred~[TAG_MODIFIER_SACRED] : ~Righteous Fury~[TAG_SPELLS_RIGHTEOUS_FURY] Bonus")
    return 0

def righteousFurySpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spell_id = args.get_arg(0)
    duration = 600 #duration is up to 1 hour; meaningless though, as duration can't be longer than spell duration atm due to Spell_End I think
    tempHpAmount = min((5 * spellPacket.caster_level), 50) #capped at cl 10 for 50 hp
    attachee.condition_add_with_args('Temporary_Hit_Points', spell_id, duration, tempHpAmount)
    print "used spell_id: {}".format(spell_id)
    return 0

righteousFurySpell = PythonModifier("sp-Righteous Fury", 3) # spell_id, duration, tempHitPoints
righteousFurySpell.AddHook(ET_OnConditionAdd, EK_NONE, righteousFurySpellOnConditionAdd,())
righteousFurySpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_STRENGTH, righteousFurySpellAbilityBonus,())
righteousFurySpell.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, spell_utils.removeTempHp, ())
righteousFurySpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
righteousFurySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
righteousFurySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
righteousFurySpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
righteousFurySpell.AddSpellDispelCheckStandard()
righteousFurySpell.AddSpellTeleportPrepareStandard()
righteousFurySpell.AddSpellTeleportReconnectStandard()
righteousFurySpell.AddSpellCountdownStandardHook()

