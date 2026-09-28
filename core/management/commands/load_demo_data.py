import random
from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (SiteSettings, CoachingService, CoachingProgram,
                         Testimonial, FAQ, Achievement)
from students.models import Student, Parent
from coaching.models import Batch, ChessClass, Attendance
from enquiries.models import Enquiry, EnquiryFollowUp
from fees.models import FeePlan, Invoice, Payment, PaymentReminder
from progress.models import ProgressEntry, Goal
from assignments.models import Assignment, AssignmentSubmission
from tournaments.models import TournamentResult
from announcements.models import Announcement


class Command(BaseCommand):
    help = 'Load realistic demo data for the chess coaching platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')

        # Superuser
        if not User.objects.filter(username='coach').exists():
            User.objects.create_superuser('coach', 'coach@chessacademy.com', 'chess123',
                                          first_name='Vikram', last_name='Sharma')
            self.stdout.write(self.style.SUCCESS('Created superuser: coach / chess123'))
        else:
            coach = User.objects.get(username='coach')
            coach.set_password('chess123')
            coach.save()

        # Site Settings
        settings = SiteSettings.load()
        settings.academy_name = 'Grandmaster Chess Academy'
        settings.coach_name = 'Coach Vikram Sharma'
        settings.tagline = 'Master the Royal Game'
        settings.about = 'Grandmaster Chess Academy is a premier chess coaching institution dedicated to developing chess talent at every level, from eager beginners to titled tournament champions.'
        settings.email = 'coach@grandmasterchess.in'
        settings.phone = '+91 98765 43210'
        settings.whatsapp = '919876543210'
        settings.address = '42 Chess Lane, Koramangala, Bangalore 560034'
        settings.hero_title = 'Elevate Your Chess Game'
        settings.hero_subtitle = 'Expert coaching from a FIDE-rated player. Personalized training for beginners to tournament players. Join 500+ students who transformed their game.'
        settings.hero_cta_text = 'Book a Free Trial'
        settings.coach_title = 'FIDE Rated Coach & International Arbiter'
        settings.coach_bio = 'With over 15 years of coaching experience, Coach Vikram has trained state and national level champions. A FIDE-rated player with a peak rating of 2150, he combines deep chess knowledge with modern teaching methods to bring out the best in every student.'
        settings.coach_experience = '15+ Years Experience'
        settings.coach_rating = '2150 FIDE'
        settings.coach_students_trained = '500+'
        settings.currency_symbol = '₹'
        settings.currency_code = 'INR'
        settings.save()
        self.stdout.write(self.style.SUCCESS('Created site settings'))

        # Services
        services_data = [
            ('Personal 1-on-1 Coaching', 'one-on-one', 'Tailored individual sessions focusing on your specific needs, weaknesses, and goals.', 'bi-person-video3', 1),
            ('Group Coaching', 'group', 'Learn alongside peers in small, focused groups. Great for competitive practice and motivation.', 'bi-people', 2),
            ('Beginner Coaching', 'beginner', 'Start your chess journey with structured lessons covering rules, basic tactics, and opening principles.', 'bi-star', 3),
            ('Intermediate Coaching', 'intermediate', 'Deepen your understanding with advanced tactics, strategy, and positional play.', 'bi-lightning', 4),
            ('Advanced / Tournament Coaching', 'advanced', 'Intensive training for serious competitors. Opening preparation, endgame mastery, and tournament strategy.', 'bi-trophy', 5),
            ('Online and Offline Coaching', 'online-offline', 'High-quality coaching available both in-person at our Koramangala academy and online worldwide.', 'bi-laptop', 6),
            ('Opening Preparation', 'opening-prep', 'Build a solid opening repertoire tailored to your style. Learn key variations and typical plans.', 'bi-book', 7),
            ('Middlegame Training', 'middlegame', 'Master planning, piece coordination, pawn structures, and strategic decision-making.', 'bi-puzzle', 8),
            ('Endgame Training', 'endgame', 'From basic checkmates to complex endgames. The most practical way to win more games.', 'bi-bullseye', 9),
            ('Tactical Training', 'tactical', 'Sharpen your calculation and pattern recognition. Daily puzzles and themed exercises.', 'bi-lightning-charge', 10),
            ('Game Analysis', 'game-analysis', 'Detailed review of your games with expert annotations. Learn from your mistakes and build on your strengths.', 'bi-search', 11),
            ('Kids Coaching', 'kids', 'Fun, engaging chess classes designed for children aged 5-15. Build thinking skills while having fun.', 'bi-emoji-smile', 12),
            ('Adult Coaching', 'adults', 'Never too late to learn. Flexible scheduling and patient instruction for adult learners.', 'bi-person-workspace', 13),
        ]
        for title, slug, desc, icon, order in services_data:
            CoachingService.objects.update_or_create(slug=slug, defaults={
                'title': title, 'description': desc, 'icon': icon, 'order': order, 'is_active': True
            })

        # Programs
        programs_data = [
            ('Beginner Foundation', 'beginner-foundation', 'Perfect for new players learning the basics of chess.', '4 classes per month\nPersonalized attention\nBasic tactics training\nOnline resources access\nProgress tracking', '₹2,000/month', False, 1),
            ('Intermediate Accelerator', 'intermediate-accelerator', 'For players rated 800-1400 looking to improve rapidly.', '8 classes per month\n1-on-1 coaching\nOpening repertoire\nGame analysis\nTournament guidance\nHomework & puzzles', '₹4,000/month', True, 2),
            ('Tournament Champion', 'tournament-champion', 'Intensive training for competitive and tournament players.', '12 classes per month\nAdvanced strategy\nOpening preparation\nEndgame training\nTournament preparation\nPost-game analysis\nOnline practice sessions', '₹6,000/month', False, 3),
            ('Elite Coaching', 'elite-coaching', 'Premium 1-on-1 coaching for serious players above 1600.', 'Unlimited sessions\nCustom training plan\nDaily puzzles\nOpening database access\n24/7 support\nTournament accompaniment', 'Contact for pricing', False, 4),
        ]
        for name, slug, desc, features, price, popular, order in programs_data:
            CoachingProgram.objects.update_or_create(slug=slug, defaults={
                'name': name, 'description': desc, 'features': features,
                'price_label': price, 'is_popular': popular, 'order': order, 'is_active': True
            })

        # Testimonials
        testimonials_data = [
            ('Priya Mehta', 'Parent', "My son's rating jumped from 900 to 1400 in just 8 months under Coach Vikram's guidance. The personalized attention and structured approach made all the difference.", 5),
            ('Arjun Reddy', 'Tournament Player', "Coach Vikram helped me prepare for the state championship. His opening preparation and endgame training were exceptional. Won 2nd place!", 5),
            ('Sneha Iyer', 'Adult Learner', "I started learning chess at 35 and was nervous, but Coach Vikram made it enjoyable and challenging. I can now hold my own in club games.", 5),
            ('Rahul Nair', 'Student', "The group classes are super fun and competitive. I love the puzzle challenges and tournament simulations.", 4),
            ('Dr. Sunita Patel', 'Parent', "Both my children attend the academy. The improvement in their concentration and problem-solving skills extends well beyond chess.", 5),
        ]
        for name, role, content, rating in testimonials_data:
            Testimonial.objects.update_or_create(name=name, defaults={
                'role': role, 'content': content, 'rating': rating, 'is_active': True
            })

        # FAQs
        faqs_data = [
            ('What age groups do you teach?', 'We teach students from age 5 to adults. Our programs are tailored for each age group with appropriate teaching methods and materials.', 1),
            ('Do I need any prior chess knowledge?', 'Not at all! We welcome absolute beginners. Our beginner program starts from the very basics - how the pieces move, basic rules, and fundamental concepts.', 2),
            ('How are online classes conducted?', 'Online classes are conducted via Zoom/Google Meet with screen sharing. We use Lichess and Chess.com for interactive practice during sessions.', 3),
            ('What is the class schedule?', 'We offer flexible scheduling. Group batches run on fixed days (Mon/Wed/Fri or Tue/Thu/Sat). Individual classes can be scheduled at your convenience.', 4),
            ('How do I track my child\'s progress?', 'We provide regular progress updates through our parent portal. You can track attendance, homework, skill development, and tournament results.', 5),
            ('Do you help with tournament preparation?', 'Yes! We provide comprehensive tournament preparation including opening analysis, time management strategies, and psychological preparation.', 6),
            ('What is your cancellation policy?', 'Classes can be rescheduled with 24 hours notice. Monthly fees are non-refundable, but unused classes can be carried forward with prior intimation.', 7),
            ('How can I pay the fees?', 'We accept payments via UPI, bank transfer, cash, and cards. Monthly fees are due by the 5th of each month.', 8),
        ]
        for q, a, order in faqs_data:
            FAQ.objects.update_or_create(question=q, defaults={'answer': a, 'order': order, 'is_active': True})

        # Achievements
        achievements_data = [
            ('State Championship Winner 2024', '3 students won medals at the Karnataka State Chess Championship', date(2024, 8, 15)),
            ('100+ Students Rated Above 1200', 'Milestone achieved in developing rated players', date(2024, 6, 1)),
            ('National Level Qualifier', '5 students qualified for the National Under-16 Championship', date(2024, 3, 20)),
            ('Best Chess Academy Award', 'Recognized as the best chess coaching academy in Bangalore', date(2023, 12, 10)),
        ]
        for title, desc, dt in achievements_data:
            Achievement.objects.update_or_create(title=title, defaults={
                'description': desc, 'date': dt, 'is_active': True
            })

        # Batches
        batches = []
        batch_data = [
            ('Beginners Batch A', 'beginner', 'offline', 'Mon/Wed/Fri 4:00-5:00 PM', 8),
            ('Beginners Batch B', 'beginner', 'online', 'Tue/Thu 5:00-6:00 PM', 10),
            ('Intermediate Batch', 'intermediate', 'offline', 'Mon/Wed/Fri 5:00-6:30 PM', 8),
            ('Advanced Batch', 'advanced', 'offline', 'Sat/Sun 10:00-12:00 PM', 6),
            ('Online Intermediate', 'intermediate', 'online', 'Tue/Thu/Sat 6:00-7:00 PM', 12),
        ]
        for name, level, mode, schedule, max_s in batch_data:
            b, _ = Batch.objects.update_or_create(name=name, defaults={
                'level': level, 'mode': mode, 'schedule': schedule, 'max_students': max_s, 'is_active': True
            })
            batches.append(b)

        # Students
        today = date.today()
        students_data = [
            ('Aarav', 'Kumar', 'male', date(2014, 3, 15), 'beginner', 'individual', 'offline', None),
            ('Ananya', 'Sharma', 'female', date(2012, 7, 22), 'intermediate', 'group', 'offline', 2),
            ('Rohan', 'Gupta', 'male', date(2011, 1, 10), 'advanced', 'both', 'offline', 3),
            ('Ishita', 'Verma', 'female', date(2013, 9, 5), 'beginner', 'group', 'offline', 0),
            ('Aryan', 'Patel', 'male', date(2010, 5, 18), 'tournament', 'individual', 'offline', None),
            ('Diya', 'Nair', 'female', date(2015, 11, 30), 'absolute_beginner', 'group', 'online', 1),
            ('Kabir', 'Singh', 'male', date(2009, 2, 14), 'intermediate', 'group', 'offline', 4),
            ('Meera', 'Joshi', 'female', date(2012, 8, 7), 'intermediate', 'group', 'online', 4),
            ('Dev', 'Reddy', 'male', date(2013, 4, 25), 'beginner', 'group', 'offline', 0),
            ('Saanvi', 'Iyer', 'female', date(2014, 12, 3), 'beginner', 'individual', 'online', None),
            ('Vihaan', 'Chopra', 'male', date(2008, 6, 19), 'advanced', 'both', 'offline', 3),
            ('Aadya', 'Menon', 'female', date(2016, 10, 8), 'absolute_beginner', 'group', 'online', 1),
        ]

        students = []
        for i, (first, last, gender, dob, level, ctype, mode, batch_idx) in enumerate(students_data):
            joining = today - timedelta(days=random.randint(60, 365))
            s, _ = Student.objects.update_or_create(
                first_name=first, last_name=last,
                defaults={
                    'gender': gender, 'date_of_birth': dob,
                    'chess_level': level, 'coaching_type': ctype,
                    'preferred_mode': mode, 'joining_date': joining,
                    'batch': batches[batch_idx] if batch_idx is not None else None,
                    'status': 'active',
                    'phone': f'+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}',
                    'email': f'{first.lower()}.{last.lower()}@example.com',
                    'school': random.choice(['DPS', 'Kendriya Vidyalaya', 'Ryan International', 'National Public School', 'St. Xaviers']),
                    'fide_rating': random.choice([800, 950, 1100, 1250, 1400, 1600, 1800]) if level in ['intermediate', 'advanced', 'tournament'] else None,
                    'chess_com_username': f'{first.lower()}_{last.lower()}',
                    'lichess_username': f'{first.lower()}{last.lower()}',
                    'strengths': random.choice(['Tactical vision', 'Opening preparation', 'Endgame technique', 'Calculation speed', 'Solid positional play']),
                    'weaknesses': random.choice(['Time trouble in blitz', 'Rook endgames', 'Defensive counterplay', 'Complex pawn structures']),
                    'chess_goals': random.choice(['Cross 1500 rating', 'Win school tournament', 'Master King\'s Indian Defense', 'Compete in National U-15']),
                    'preferred_openings': random.choice(['Italian Game, Caro-Kann', 'Sicilian Defense, Queen\'s Gambit', 'Ruy Lopez, French Defense', 'London System, King\'s Indian']),
                    'notes': f'Hardworking student with consistent attendance.'
                }
            )
            students.append(s)

        # Parents
        parent_names = [
            ('Rajesh Kumar', 'father', 0), ('Priya Kumar', 'mother', 0),
            ('Amit Sharma', 'father', 1), ('Neha Gupta', 'mother', 2),
            ('Suresh Verma', 'father', 3), ('Deepa Patel', 'mother', 4),
            ('Anil Nair', 'father', 5), ('Sunita Singh', 'mother', 6),
            ('Manoj Joshi', 'father', 7), ('Kavita Reddy', 'mother', 8),
            ('Sanjay Iyer', 'father', 9), ('Geeta Chopra', 'mother', 10),
        ]

        parents = []
        for name, rel, student_idx in parent_names:
            p, _ = Parent.objects.update_or_create(
                name=name, defaults={
                    'relationship': rel,
                    'phone': f'+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}',
                    'whatsapp': f'91{random.randint(7000000000, 9999999999)}',
                    'email': f'{name.lower().replace(" ", ".")}@example.com',
                    'preferred_communication': random.choice(['whatsapp', 'phone', 'email']),
                }
            )
            p.students.add(students[student_idx])
            parents.append(p)

        # Portal Users
        for s in students[:4]:
            uname = f'{s.first_name.lower()}.{s.last_name.lower()}'
            u, _ = User.objects.get_or_create(username=uname, defaults={
                'first_name': s.first_name, 'last_name': s.last_name, 'email': s.email
            })
            u.set_password('chess123')
            u.save()
            s.user = u
            s.save()

        p_sample = parents[0]
        p_uname = 'parent.rajesh'
        pu, _ = User.objects.get_or_create(username=p_uname, defaults={
            'first_name': 'Rajesh', 'last_name': 'Kumar', 'email': p_sample.email
        })
        pu.set_password('chess123')
        pu.save()
        p_sample.user = pu
        p_sample.save()

        # Fee Plans
        fee_plans = []
        plan_data = [
            ('Beginner Monthly', 'Monthly fee for beginner batch', 2000, 'monthly'),
            ('Intermediate Monthly', 'Monthly fee for intermediate batch', 4000, 'monthly'),
            ('Advanced Monthly', 'Monthly fee for advanced batch', 6000, 'monthly'),
            ('Individual Session Package', 'Individual coaching (4 sessions)', 3200, 'monthly'),
            ('Tournament Intensive', 'Quarterly tournament preparation', 12000, 'quarterly'),
        ]
        for name, desc, amount, freq in plan_data:
            fp, _ = FeePlan.objects.update_or_create(name=name, defaults={
                'description': desc, 'amount': amount, 'frequency': freq, 'is_active': True
            })
            fee_plans.append(fp)

        # Invoices and Payments
        for s in students:
            plan = fee_plans[0] if s.chess_level in ['beginner', 'absolute_beginner'] else (fee_plans[1] if s.chess_level == 'intermediate' else fee_plans[2])
            for m_offset in [2, 1, 0]:
                inv_month = today.replace(day=1) - timedelta(days=30 * m_offset)
                due_d = inv_month.replace(day=5)
                desc = f'Coaching Fee - {inv_month.strftime("%B %Y")}'
                
                inv, _ = Invoice.objects.update_or_create(
                    student=s, description=desc,
                    defaults={
                        'fee_plan': plan,
                        'amount': plan.amount,
                        'amount_paid': 0,
                        'due_date': due_d,
                        'status': 'pending',
                        'notes': 'Monthly tuition fee'
                    }
                )
                
                if m_offset == 2:
                    # Fully paid
                    Payment.objects.get_or_create(
                        invoice=inv, amount=inv.amount,
                        defaults={
                            'payment_date': due_d - timedelta(days=2),
                            'method': 'upi',
                            'reference': f'UPI{random.randint(10000000, 99999999)}',
                            'notes': 'Paid on time'
                        }
                    )
                elif m_offset == 1:
                    # Half paid or paid
                    if random.random() > 0.3:
                        Payment.objects.get_or_create(
                            invoice=inv, amount=inv.amount,
                            defaults={
                                'payment_date': due_d + timedelta(days=3),
                                'method': 'bank_transfer',
                                'reference': f'NEFT{random.randint(100000, 999999)}'
                            }
                        )
                    else:
                        Payment.objects.get_or_create(
                            invoice=inv, amount=inv.amount / 2,
                            defaults={
                                'payment_date': due_d + timedelta(days=5),
                                'method': 'cash',
                                'reference': 'CASH-REC-01'
                            }
                        )
                elif m_offset == 0:
                    # Current month: some pending, some paid
                    if random.random() > 0.6:
                        Payment.objects.get_or_create(
                            invoice=inv, amount=inv.amount,
                            defaults={
                                'payment_date': today,
                                'method': 'upi',
                                'reference': f'UPI{random.randint(10000000, 99999999)}'
                            }
                        )
                inv.update_status()

        # Classes and Attendance
        for d in range(20, -1, -1):
            c_date = today - timedelta(days=d)
            if c_date.weekday() in [0, 2, 4]: # Mon, Wed, Fri
                b = batches[0]
                cls, _ = ChessClass.objects.update_or_create(
                    date=c_date, start_time=time(16, 0), batch=b,
                    defaults={
                        'title': f'{b.name} - Session',
                        'class_type': 'group',
                        'mode': b.mode,
                        'end_time': time(17, 0),
                        'topic': random.choice(['Pin and Skewer tactics', 'King & Pawn Endgame', 'Developing Pieces Safely', 'Defending checkmates']),
                        'homework': 'Solve 10 tactical exercises on Lichess',
                        'coach_notes': 'All students participated well.',
                        'status': 'completed' if d > 0 else 'scheduled'
                    }
                )
                cls.students.set(b.students.filter(status='active'))
                if cls.status == 'completed':
                    for st in cls.students.all():
                        Attendance.objects.update_or_create(
                            chess_class=cls, student=st,
                            defaults={'status': random.choices(['present', 'late', 'absent'], weights=[80, 10, 10])[0]}
                        )
            elif c_date.weekday() in [1, 3]: # Tue, Thu
                b = batches[2]
                cls, _ = ChessClass.objects.update_or_create(
                    date=c_date, start_time=time(17, 0), batch=b,
                    defaults={
                        'title': f'{b.name} - Deep Dive',
                        'class_type': 'group',
                        'mode': b.mode,
                        'end_time': time(18, 30),
                        'topic': random.choice(['Sicilian Defense Dragon', 'Rook + Bishop vs Rook', 'Positional Pawn Sacrifices', 'Calculation Trees']),
                        'homework': 'Analyze 3 master games in the Sicilian Dragon',
                        'coach_notes': 'Good tactical calculation shown today.',
                        'status': 'completed' if d > 0 else 'scheduled'
                    }
                )
                cls.students.set(b.students.filter(status='active'))
                if cls.status == 'completed':
                    for st in cls.students.all():
                        Attendance.objects.update_or_create(
                            chess_class=cls, student=st,
                            defaults={'status': random.choices(['present', 'late', 'absent'], weights=[85, 10, 5])[0]}
                        )

        # Future classes
        for d in range(1, 10):
            f_date = today + timedelta(days=d)
            if f_date.weekday() in [0, 2, 4]:
                b = batches[0]
                cls, _ = ChessClass.objects.update_or_create(
                    date=f_date, start_time=time(16, 0), batch=b,
                    defaults={
                        'title': f'{b.name} - Upcoming',
                        'class_type': 'group',
                        'mode': b.mode,
                        'end_time': time(17, 0),
                        'topic': 'Discovered Attacks and Double Checks',
                        'homework': 'Practice puzzle streak',
                        'status': 'scheduled'
                    }
                )
                cls.students.set(b.students.filter(status='active'))

        # Enquiries
        enquiries_data = [
            ('Kavya Rao', 'Sunita Rao', 8, '+91 98450 12345', 'sunita@example.com', 'beginner', 'new', 'Interested in starting weekend chess classes for my 8-year-old daughter.'),
            ('Aditya Menon', 'Ramesh Menon', 12, '+91 98451 23456', 'ramesh@example.com', 'intermediate', 'contacted', 'Rated around 1100 on Chess.com. Looking to play FIDE tournaments.'),
            ('Tanvi Desai', 'Pooja Desai', 10, '+91 98452 34567', 'pooja@example.com', 'beginner', 'trial_scheduled', 'Booked trial class for this Saturday.'),
            ('Nikhil Jain', '', 28, '+91 98453 45678', 'nikhil.jain@example.com', 'advanced', 'interested', 'Adult player rated 1650 on Lichess. Need opening prep against 1.d4.'),
            ('Riya Kapoor', 'Ankit Kapoor', 7, '+91 98454 56789', 'ankit@example.com', 'absolute_beginner', 'new', 'Looking for beginner batches in Koramangala center.'),
            ('Siddharth Das', '', 34, '+91 98455 67890', 'sid.das@example.com', 'beginner', 'follow_up', 'Wants online classes after 8 PM on weekdays.'),
            ('Neha Malhotra', 'Vivek Malhotra', 11, '+91 98456 78901', 'vivek@example.com', 'intermediate', 'not_interested', 'Schedule did not match their school timings.'),
        ]
        for sname, pname, age, phone, email, level, status, msg in enquiries_data:
            enq, _ = Enquiry.objects.update_or_create(
                student_name=sname,
                defaults={
                    'parent_name': pname, 'age': age, 'phone': phone, 'whatsapp': phone.replace(' ', '').replace('+', ''),
                    'email': email, 'current_level': level, 'status': status, 'message': msg,
                    'preferred_mode': 'offline' if age < 10 else 'both',
                    'coaching_goal': 'Improve rating and tournament confidence',
                    'follow_up_date': today + timedelta(days=2) if status == 'follow_up' else None
                }
            )
            if status in ['contacted', 'trial_scheduled', 'interested']:
                EnquiryFollowUp.objects.get_or_create(
                    enquiry=enq,
                    defaults={'notes': f'Spoke to parent. Explained syllabus and fee structure. Positive response.', 'next_follow_up': today + timedelta(days=3)}
                )

        # Progress Entries
        for s in students[:6]:
            ProgressEntry.objects.update_or_create(
                student=s, date=today - timedelta(days=30),
                defaults={
                    'rating': (s.fide_rating or 1000) - 40,
                    'tactics': random.randint(6, 8),
                    'opening_knowledge': random.randint(5, 7),
                    'middlegame': random.randint(6, 8),
                    'endgame': random.randint(5, 7),
                    'calculation': random.randint(6, 8),
                    'positional': random.randint(5, 7),
                    'time_management': random.randint(6, 8),
                    'strengths': 'Tactical alertness, quick calculations',
                    'weaknesses': 'Rushed moves in winning positions',
                    'next_goals': 'Focus on calculating candidate moves systematically',
                    'coach_comments': 'Showing steady improvement. Great discipline in homework.'
                }
            )
            ProgressEntry.objects.update_or_create(
                student=s, date=today - timedelta(days=5),
                defaults={
                    'rating': s.fide_rating or 1000,
                    'tactics': random.randint(7, 9),
                    'opening_knowledge': random.randint(7, 9),
                    'middlegame': random.randint(7, 8),
                    'endgame': random.randint(6, 8),
                    'calculation': random.randint(7, 9),
                    'positional': random.randint(6, 8),
                    'time_management': random.randint(7, 9),
                    'strengths': 'Strong calculation and deep endgame understanding',
                    'weaknesses': 'Passive defense against flank attacks',
                    'next_goals': 'Work on dynamic defense and pawn sacrifices',
                    'coach_comments': 'Excellent month. Scored well in the local tournament.'
                }
            )

        # Goals
        for s in students[:6]:
            Goal.objects.update_or_create(
                student=s, title='Attain 1400 FIDE Rating',
                defaults={
                    'description': 'Participate in at least 3 rated tournaments this quarter.',
                    'priority': 'high',
                    'status': 'in_progress',
                    'progress_percent': 65,
                    'target_date': today + timedelta(days=90),
                    'coach_notes': 'On track! Keep solving 20 puzzles daily.'
                }
            )
            Goal.objects.update_or_create(
                student=s, title='Complete Endgame Repertoire',
                defaults={
                    'description': 'Master Rook + Pawn endgames, Lucena and Philidor positions.',
                    'priority': 'medium',
                    'status': 'completed',
                    'progress_percent': 100,
                    'target_date': today - timedelta(days=5),
                    'completed_date': today - timedelta(days=5),
                    'coach_notes': 'Successfully demonstrated all key positions.'
                }
            )

        # Assignments
        hw1, _ = Assignment.objects.update_or_create(
            title='Tactics: Deflection & Decoy Puzzles',
            defaults={
                'description': 'Solve the 25 exercises from Chapter 4 of the tactics workbook. Focus on calculating until the final checkmate or piece capture.',
                'due_date': today + timedelta(days=4),
                'batch': batches[0],
                'coach_notes': 'Do not guess! Write down variations in notation.'
            }
        )
        hw1.students.set(batches[0].students.all())
        for st in batches[0].students.all():
            AssignmentSubmission.objects.get_or_create(
                assignment=hw1, student=st,
                defaults={'status': 'pending'}
            )

        hw2, _ = Assignment.objects.update_or_create(
            title='Annotate Your Best Game from the Weekend',
            defaults={
                'description': 'Take your 15-minute rapid game from Sunday, analyze it without an engine first, and identify your critical inaccuracies.',
                'due_date': today - timedelta(days=2),
                'batch': batches[2],
                'coach_notes': 'Good analysis by most students.'
            }
        )
        hw2.students.set(batches[2].students.all())
        for st in batches[2].students.all():
            AssignmentSubmission.objects.get_or_create(
                assignment=hw2, student=st,
                defaults={'status': 'completed', 'coach_feedback': 'Great effort in identifying the mistake on move 22.'}
            )

        # Tournament Results
        TournamentResult.objects.update_or_create(
            student=students[1], tournament_name='Bangalore Junior Rapid Championship 2024',
            date=today - timedelta(days=25),
            defaults={
                'location': 'Kanteerava Stadium, Bangalore',
                'total_rounds': 6,
                'score': '5.0/6',
                'rank': 3,
                'total_participants': 84,
                'rating_before': 1180,
                'rating_after': 1245,
                'performance_rating': 1360,
                'highlights': 'Undefeated until the final round! Outstanding endgame play in Round 4.',
                'coach_notes': 'Strong performance. Needs to prepare more against the English Opening.'
            }
        )
        TournamentResult.objects.update_or_create(
            student=students[2], tournament_name='Karnataka State Under-15 Selection',
            date=today - timedelta(days=40),
            defaults={
                'location': 'Mysore',
                'total_rounds': 7,
                'score': '5.5/7',
                'rank': 5,
                'total_participants': 120,
                'rating_before': 1390,
                'rating_after': 1435,
                'performance_rating': 1510,
                'highlights': 'Qualified for the state coaching camp! Brilliant tactical win against seed #4.',
                'coach_notes': 'Very mature positional handling.'
            }
        )

        # Announcements
        Announcement.objects.update_or_create(
            title='Karnataka State Under-14 Championship Registrations Open!',
            defaults={
                'content': 'All interested tournament batch players please register by next Wednesday. We will have dedicated prep sessions on Friday afternoon.',
                'audience': 'everyone',
                'priority': 'high',
                'is_active': True
            }
        )
        Announcement.objects.update_or_create(
            title='Upcoming Friendly Blitz Tournament this Saturday',
            defaults={
                'content': 'We will host an internal blitz arena (3+2) on Lichess this Saturday at 6:00 PM IST. Exciting chess book prizes for the top 3 finishers!',
                'audience': 'students',
                'priority': 'normal',
                'is_active': True
            }
        )

        # Payment Reminders
        for inv in Invoice.objects.filter(status__in=['pending', 'overdue'])[:3]:
            parent = inv.student.parents.first()
            if parent:
                PaymentReminder.objects.update_or_create(
                    invoice=inv,
                    defaults={
                        'reminder_type': 'whatsapp',
                        'scheduled_date': today + timedelta(days=2),
                        'message': f'Hello {parent.name}, this is a friendly reminder that the chess coaching fee of ₹{inv.balance} for {inv.student.full_name} is pending. Due date: {inv.due_date.strftime("%d %b %Y")}. Thank you.',
                        'status': 'pending'
                    }
                )

        self.stdout.write(self.style.SUCCESS('\n======================================================='))
        self.stdout.write(self.style.SUCCESS('🎉 Demo data successfully created and loaded!'))
        self.stdout.write(self.style.SUCCESS('======================================================='))
        self.stdout.write('\nUser Accounts created:')
        self.stdout.write('  1. Coach (Admin):    Username: coach           Password: chess123')
        self.stdout.write('  2. Student:          Username: aarav.kumar     Password: chess123')
        self.stdout.write('  3. Parent:           Username: parent.rajesh   Password: chess123')
        self.stdout.write('\nVisit: http://127.0.0.1:8000/')
