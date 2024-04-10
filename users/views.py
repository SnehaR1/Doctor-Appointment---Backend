from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserData
import pyotp
from django.core.mail import send_mail
from django.conf import settings
from django.forms.models import model_to_dict

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):

        try:
            refreshToken = request.data.get("refreshToken")

            if refreshToken:
                RefreshToken(refreshToken).blacklist()
                return Response(
                    {"message ": "The user logged out successfully"},
                    status=status.HTTP_205_RESET_CONTENT,
                )
            else:
                return Response(
                    {"error": "The RefreshToken was not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Something went Erong {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetEmail(APIView):
    def post(self, request):
        email = request.data.get("email")
        print(email)
        if email.strip() == "":
            return Response({"error": "Enter a Valid Email"})
        try:
            user = UserData.objects.filter(email=email).first()
            print(user)
            if user:
                otp = self.generateOtp()
                print(otp)

                request.session["otp"] = otp
                request.session["email"] = email
                request.session.save()

                self.sendMail(otp, email)
                return Response(
                    {"message": "OTP successfully sent to the provided Email"},
                    status=status.HTTP_205_RESET_CONTENT,
                )
            else:
                return Response({"error": "No User with that Email exists"})
        except Exception as e:
            print(str(e))
            return Response({"error": f"Something went Wrong!"})

    def sendMail(self, otp, email):
        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )

    def generateOtp(self):
        totp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(totp_secret, interval=60)
        otp = totp.now()
        return otp


class OTPVerification(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        print(otp)

        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        session_otp = request.session.get("otp")
        print(session_otp)
        try:
            if session_otp == otp:

                user = UserData.objects.filter(
                    email=request.session.get("email")
                ).first()

                if user:
                    if password == confirm_password:
                        user.set_password(password)
                        user.save()
                        request.session.clear()
                        request.session.save()

                        return Response(
                            {"message": "Password Successfully changed"},
                            status=status.HTTP_205_RESET_CONTENT,
                        )
                    else:
                        return Response({"error": "Passwords don't match"})
                else:
                    return Response({"error": "Something went wrong"})
            else:
                return Response({"error": "OTP Entered Is Wrong or Expired"})
        except UserData.DoesNotExist:
            return Response({"error": "User does not exist"})
        except Exception as e:
            print(str(e))
            return Response({"error": "Internal Server Error"})
