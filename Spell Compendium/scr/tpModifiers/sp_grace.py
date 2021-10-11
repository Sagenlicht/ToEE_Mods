from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Grace"

def graceSpellPenaltyToHide(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-20, 21, "~Circumstance~[TAG_MODIFIER_CIRCUMSTANCE] : ~Grace~[TAG_SPELLS_GRACE") #Grace adds a -20 penalty to Hide checks
    return 0

def graceSpellBonusToDexterity(attachee, args, evt_obj):
    evt_obj.bonus_list.add(2, 153, "~Sacred~[TAG_MODIFIER_SACRED] : ~Grace~[TAG_SPELLS_GRACE]") #Grace gives a +2 sacred bonus to Dexterity
    return 0

def graceSpellBonusToMovement(attachee, args, evt_obj):
    evt_obj.bonus_list.add(10, 0, "~Grace~[TAG_SPELLS_GRACE] Bonus") #Grace adds 10 to the movement speed
    return 0

def graceSpellAddGoodProperty(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    if not evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        if evt_obj.damage_packet.attack_power & D20DAP_HOLY:
            return 0
        elif evt_obj.damage_packet.attack_power & D20DAP_UNHOLY:
            evt_obj.damage_packet.attack_power -= D20DAP_UNHOLY
        elif evt_obj.damage_packet.attack_power & D20DAP_LAW:
            evt_obj.damage_packet.attack_power -= D20DAP_LAW
        elif evt_obj.damage_packet.attack_power & D20DAP_CHAOS:
            evt_obj.damage_packet.attack_power -= D20DAP_CHAOS
        evt_obj.damage_packet.attack_power |= D20DAP_HOLY
    return 0

def graceSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Grace ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Grace ({} rounds)".format(args.get_arg(1)))
    return 0

def graceSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("GRACE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("GRACE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def graceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def graceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def graceSpellSpellEnd(attachee, args, evt_obj):
    print "Grace SpellEnd"
    return 0

graceSpell = PythonModifier("sp-Grace", 2) # spell_id, duration
graceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_HIDE, graceSpellPenaltyToHide, ())
graceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, graceSpellBonusToDexterity, ())
graceSpell.AddHook(ET_OnGetMoveSpeed, EK_NONE, graceSpellBonusToMovement, ())
graceSpell.AddHook(ET_OnDealingDamage, EK_NONE, graceSpellAddGoodProperty, ())
graceSpell.AddHook(ET_OnGetTooltip, EK_NONE, graceSpellTooltip, ())
graceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, graceSpellEffectTooltip, ())
graceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, graceSpellSpellEnd, ())
graceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, graceSpellHasSpellActive, ())
graceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, graceSpellKilled, ())
graceSpell.AddSpellDispelCheckStandard()
graceSpell.AddSpellTeleportPrepareStandard()
graceSpell.AddSpellTeleportReconnectStandard()
graceSpell.AddSpellCountdownStandardHook()
