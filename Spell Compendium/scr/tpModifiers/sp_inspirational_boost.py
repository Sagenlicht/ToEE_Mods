from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Inspirational Boost"

def inspirationalBoostSpellBonus(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def inspirationalBoostSpellOnBeginRound(attachee, args, evt_obj):
    if not args.get_arg(2):
        duration = args.get_arg(1)
        duration += 1
        args.set_arg(1, duration)
    return 0

def inspirationalBoostSpellCheckExpiry(attachee, args, evt_obj):
    print "Expiry Hook"
    roundsToExpire = attachee.d20_query("Bardic Ability Duration Bonus")
    roundsToExpire += 5 #Bard songs linger 5 rounds after song ended
    if attachee.has_feat("Lingering Song"):
        print "Has Song extender Feat"
    print "roundsToExpire: {}".format(roundsToExpire)
    args.set_arg(1, roundsToExpire)
    args.set_arg(2, 1)
    return 0

def inspirationalBoostSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Inspirational Boost ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Inspirational Boost ({} rounds)".format(args.get_arg(1)))
    return 0

def inspirationalBoostSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("INSPIRATIONAL_BOOST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("INSPIRATIONAL_BOOST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def inspirationalBoostSpellHasSpellActive(attachee, args, evt_obj):
    if evt_obj.data1 == args.get_arg(2):
        evt_obj.return_val = 1
    return 0

def inspirationalBoostSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def inspirationalBoostSpellSpellEnd(attachee, args, evt_obj):
    print "Inspirational BoostSpellEnd"
    return 0

inspirationalBoostSpell = PythonModifier("sp-Inspirational Boost", 3) # spell_id, duration. spellEnum, expiryFlag
inspirationalBoostSpell.AddHook(ET_OnD20PythonQuery, "Inspirational Boost", inspirationalBoostSpellBonus, ())
inspirationalBoostSpell.AddHook(ET_OnBeginRound, EK_NONE, inspirationalBoostSpellOnBeginRound, ())
inspirationalBoostSpell.AddHook(ET_OnD20Signal, EK_S_Bardic_Music_Completed, inspirationalBoostSpellCheckExpiry, ())
inspirationalBoostSpell.AddHook(ET_OnGetTooltip, EK_NONE, inspirationalBoostSpellTooltip, ())
inspirationalBoostSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, inspirationalBoostSpellEffectTooltip, ())
inspirationalBoostSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, inspirationalBoostSpellSpellEnd, ())
inspirationalBoostSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, inspirationalBoostSpellHasSpellActive, ())
inspirationalBoostSpell.AddHook(ET_OnD20Signal, EK_S_Killed, inspirationalBoostSpellKilled, ())
inspirationalBoostSpell.AddSpellDispelCheckStandard()
inspirationalBoostSpell.AddSpellTeleportPrepareStandard()
inspirationalBoostSpell.AddSpellTeleportReconnectStandard()
inspirationalBoostSpell.AddSpellCountdownStandardHook()
