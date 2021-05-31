from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *

# Get the spell's name from its spell_id
def spellName(spellId):
    spellEnum = tpdp.SpellPacket(spellId).spell_enum
    return game.get_spell_mesline(spellEnum)

def spellKeyName(spellId):
    return spellName(spellId).upper().replace(" ", "_")

def spellKey(spellId):
    return tpdp.hash(spellKeyName(spellId))

def spellTime(duration):
    if duration == 1:
        return "1 round"
    elif duration < 100: # 10 minutes
        return "{} rounds".format(duration)
    elif duration < 1200: # 2 hours
        return "{} minutes".format(duration/10)
    elif duration < 28800: # 2 days
        return "{} hours".format(duration/600)
    elif duration < 864000: # 2 months
        return "{} days".format(duration/14400)
    else:
        return "{} months".format(duration/432000)

### Standard Hooks invoked with AddHook ###

#[pytonModifier].AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
def spellTooltip(attachee, args, evt_obj):
    name = spellName(args.get_arg(0))
    duration = spellTime(args.get_arg(1))
    evt_obj.append("{} ({})".format(name, duration))
    return 0

#[pytonModifier].AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
def spellEffectTooltip(attachee, args, evt_obj):
    key = spellKey(args.get_arg(0))
    duration = spellTime(args.get_arg(1))
    evt_obj.append(key, -2, " ({})".format(duration))
    return 0

#[pytonModifier].AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
def queryActiveSpell(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

#[pytonModifier].AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
def spellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

#[pytonModifier].AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, spell_utils.checkRemoveSpell, ())
#[pytonModifier].AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, spell_utils.checkRemoveSpell, ())
def checkRemoveSpell(attachee, args, evt_obj):
    if evt_obj.data1 == args.get_arg(0):
        args.remove_spell()
        args.remove_spell_mod()
    return 0

#[pytonModifier].AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addConcentration, ())
def addConcentration(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.caster.condition_add_with_args('sp-Concentrating', args.get_arg(0))
    return 0

#[pytonModifier].AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addDimiss, ())
def addDimiss(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.caster.condition_add_with_args('Dismiss', args.get_arg(0))
    return 0

#[pytonModifier].AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, spell_utils.removeTempHp, ())
# needed in combination with condition_add_with_args('Temporary_Hit_Points', spell.id, spell.duration, tempHpAmount)
def removeTempHp(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
    return 0

### Other useful functions ###

# Skill Check with history windows #
def skillCheck(attachee, skillEnum, skillCheckDc):
    skillName = game.get_mesline("mes/skill.mes", skillEnum)
    bonusListSkill = tpdp.BonusList()
    skillValue = tpdp.dispatch_skill(attachee, skillEnum , bonusListSkill, OBJ_HANDLE_NULL, 1)
    skillDice = dice_new('1d20')
    skillDiceRoll = skillDice.roll()
    skillRollResult = skillDiceRoll + skillValue
    skillHistoryId = tpdp.create_history_dc_roll(attachee, skillCheckDc, skillDice, skillDiceRoll, "{}".format(skillName), bonusListSkill)
    game.create_history_from_id(skillHistoryId)
    checkResult = True if skillRollResult >= skillCheckDc else False
    return checkResult

### Utilities for defining touch attacks with held charge ###

# Keys off 'SPELL_NAME_CHARGE' so that a buff indicator for the holding
# charge state can be separated from a debuff indicator for the spell's
# effect.
def touchKey(spellId):
    return tpdp.hash("{}_CHARGE".format(spellKeyName(spellId)))

# Presumes that duration and charges are as the helper class below
def touchInfo(args):
    duration = args.get_arg(1)
    charges = args.get_arg(2)

    msgs = []
    if charges == 1:
        msgs.append("1 charge")
    elif charges > 1:
        msgs.append("{} charges".format(charges))

    if duration > 0:
        msgs.append(spellTime(duration))

    paren = ""
    if len(msgs) > 0:
        paren = " ({})".format(", ".join(msgs))

    return paren

# Handles the tooltip event for held touch spells.
def touchTooltip(attachee, args, evt_obj):
    evt_obj.append("{}{}".format(spellName(args.get_arg(0)), touchInfo(args)))
    return 0

# Handles the effect tooltip event for held touch spells.
def touchEffectTooltip(attachee, args, evt_obj):
    evt_obj.append(touchKey(args.get_arg(0)), -2, touchInfo(args))
    return 0

# Indicate which spell a character with this condition
# is holding a charge for.
def touchHoldingCharge(attachee, args, evt_obj):
    spell_id = args.get_arg(0)

    evt_obj.return_val = 1
    evt_obj.data1 = spell_id
    return 0

# if a charge attack is added, and it's not the spell _this_
# condition was added from, the spell needs to end.
def touchTouchAttackAdded(attachee, args, evt_obj):
    spell_id = args.get_arg(0)

    if evt_obj.data1 != spell_id:
        args.condition_remove()
        args.remove_spell()
    return 0

# On the round a charge is held, a free touch attack may be
# made, since it is supposed to happen as part of casting.
def touchAdd(attachee, args, evt_obj):
    spell_id = args.get_arg(0)

    tbFlags = tpdp.cur_seq_get_turn_based_status_flags()
    tbFlags = tbFlags | TBSF_TouchAttack
    tpdp.cur_seq_set_turn_based_status_flags(tbFlags)
    attachee.d20_send_signal(S_TouchAttackAdded, spell_id)
    return 0

# End the spell and remove the holding-charge condition.
def End(attachee, args, evt_obj):
    args.condition_remove()
    args.remove_spell()
    return 0

# Common code for handling touch attack charges.
#
# 1) Decrements number of charges if positive
# 2) Ends the condition if charges fall to 0
# 3) Checks spell resistance on the target.
# 4) If resistance fails, adds the target to the
#        spell's target list
#
# Returns whether the spell was resisted so that
# further effects can be run.
#
# Common use would be something like:
#
#  def OnTouch(attachee, args, evt_obj):
#    resisted = touchPre(args, evt_obj)
#
#    if not resisted:
#      <spell effects>
def touchPre(args, evt_obj):
    action = evt_obj.get_d20_action()
    caster = action.performer
    target = action.target

    spell_id = args.get_arg(0)
    duration = args.get_arg(1)
    charges = args.get_arg(2)

    packet = tpdp.SpellPacket(spell_id)

    if charges > 0:
        args.set_arg(2, charges-1)

    resisted = packet.check_spell_resistance(target)

    if charges == 1:
        packet.end_target_particles(caster)
        packet.remove_target(caster)
        args.condition_remove()

    if resisted:
        game.particles('Fizzle', target)
        game.sound(7461,1)
    else:
        packet.add_target(target, 0)

    packet.update_registry()
    if packet.target_count <= 0:
        args.spell_remove()

    return resisted

# Modifiers representing a 'held charge' touch spell
class TouchModifier(PythonModifier):
    # Touch modifiers have at least 3 arguments
    #
    #  0: spell_id
    #  1: duration, -1 to not display
    #  2: num_charges, -1 for until duration expires
    #
    # the given argument number is for additional arguments beyond
    # this.
    #
    # The standard countdown hook is not added, since the typical
    # mechanic is for charges to be held indefinitely until used.
    # An argument is reserved for time limited touch spells,
    # however, and the countdown hook can be added in such a case.
    def __init__(self, name, argn):
        PythonModifier.__init__(self, name, 3+argn)

        self.AddHook(ET_OnGetTooltip, EK_NONE, touchTooltip, ())
        self.AddHook(ET_OnGetEffectTooltip, EK_NONE, touchEffectTooltip, ())

        # Handle queries for whether the affected creature is
        # 'holding charge'?
        self.AddHook(ET_OnD20Query, EK_Q_HoldingCharge, touchHoldingCharge, ())

        # get notifications of other charge attacks being added
        self.AddHook(
                ET_OnD20Signal, EK_S_TouchAttackAdded,
                touchTouchAttackAdded, ())

        # casting another spell ends held charge spells
        self.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, End, ())

        # modify the menus to allow for touch attacks
        self.AddHook(ET_OnConditionAdd, EK_NONE, touchAdd, ())

        self.AddHook(ET_OnNewDay, EK_NEWDAY_REST, End, ())

        self.AddSpellDispellCheckHook()
        self.AddSpellTeleportPrepareStandard()
        self.AddSpellTeleportReconnectStandard()
        self.AddSpellTouchAttackDischargeRadialMenuHook()

    def AddTouchHook(self, hook):
        self.AddHook(ET_OnD20Signal, EK_S_TouchAttack, hook, ())
